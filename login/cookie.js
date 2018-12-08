// Get the unlogin cookie by rendering the resources
const CDP = require('chrome-remote-interface');
const fs = require('fs')
const path = require('path')

let cookieReq = [];
let unlogin = {};
let reqheaders = {};
let filename = '';
let firstid = 0;
let turned = false;

function ReadReq(filename) {
    let data = fs.readFileSync(path.join('headers', 'login', filename + '.json'), 'utf-8');
    const reqJson = JSON.parse(data).available;
    for (let key in reqJson) {
        let req = reqJson[key];
        if (req.method == 'GET' && 'headers' in req && ('cookie' in req.headers || 'Cookie' in req.headers) && 'bytes' in req)
            cookieReq.push(req);
    }
}

CDP((client) => {
    // extract domains
    const { Network, Page, Security } = client;
    // console.log(Security);

    Security.setIgnoreCertificateErrors({ ignore: true });
    //Security.disable();

    // Network.requestWillBeSent(async() => {

    // });

    Network.responseReceived(params => {
        if (!turned) {
            const decision = ('headers' in params.response) && ('content-disposition' in params.response.headers 
                            || ('content-type' in params.response.headers 
                            && params.response.headers['content-type'].indexOf('octet-stream') != -1));
            if (decision) {
                cookieReq.shift();
                if (!cookieReq.length) {
                    client.close();
                    fs.writeFile(path.join('headers', 'unlogin', filename + '.json'), JSON.stringify(unlogin), 'utf-8', err => {
                        if (err) throw err;
                    });
                } else {
                    const url = cookieReq[0].url;
                    // console.log("Download: "+ url + '\n\n');
                    firstid = 0;
                    turned = false;
                    return Page.navigate({ url: url });
                }
                return;
            }
            reqheaders[params.requestId] = params.response.requestHeaders;
            firstid = params.requestId;
            turned = true;
        }
    });

    Network.loadingFinished(params => {
        if (params.requestId == firstid) {
            Page.stopLoading();
            unlogin[cookieReq[0].url] = {
                "headers": reqheaders[params.requestId]
            };
            cookieReq.shift();
            if (!cookieReq.length) {
                client.close();
                fs.writeFile(path.join('headers', 'unlogin', filename + '.json'), JSON.stringify(unlogin), 'utf-8', err => {
                    if (err) throw err;
                });
            } else {
                const url = cookieReq[0].url;
                // console.log("Finished: "+ url + '\n\n');
                firstid = 0;
                turned = false;
                return Page.navigate({ url: url });
            }
        }
    });

    // enable events then start!
    Promise.all([
        Network.enable(),
        Network.clearBrowserCache(),
        Page.enable(),
        Page.setDownloadBehavior({ behavior: 'deny' })
    ]).then(() =>{
        filename = process.argv[2];
        ReadReq(filename);
        const url = cookieReq[0].url;
        return Page.navigate({ url: url });
    }).catch((err) => {
        console.error(err);
        client.close();
    });

}).on('error', (err) => {
    // cannot connect to the remote endpoint
    console.error(err);
});

