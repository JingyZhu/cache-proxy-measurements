const CDP = require('chrome-remote-interface');
const fs = require('fs')
const parse = require('url').parse
const path = require('path')

let cookieReq = [];
let compare = { 'same': {}, 'diff': {} };
let reqheaders = {};
let filename = '';
let firstid = 0;
let turned = false;
let resource = {};
let currentUrl = '';

function ReadReq(filename) {
    let data = fs.readFileSync(path.join('headers', 'login', filename.replace(/\//g, '_') + '.json'), 'utf-8');
    const reqJson = JSON.parse(data).available;
    for (let key in reqJson) {
        let req = reqJson[key];
        if (req.method == 'GET' && 'headers' in req && ('cookie' in req.headers || 'Cookie' in req.headers) && 'bytes' in req)
            cookieReq.push(req);
    }
}

function ReadResource(filename) {
    let data = fs.readFileSync(path.join('headers', 'resources', filename.replace(/\//g, '_') + '.json'), 'utf-8');
    resource = JSON.parse(data);
}

function identical(req, body, resource){
    if (['XHR', 'Document', 'Fetch'].indexOf(req['type']) >= 0 )
        return req.bytes == body.length;
    return body == resource[req.url].body;
}

CDP((client) => {
    // extract domains
    const { Network, Page, Security } = client;
    // console.log(Security);

    Security.setIgnoreCertificateErrors({ ignore: true });
    //Security.disable();

    Network.requestWillBeSent(params => {
        //console.log("request: " + params.requestId);
        
        if (params.documentURL == currentUrl && !turned){
            firstid = params.requestId;
            turned = true;
        }
     });

    Network.responseReceived(params => {
        // console.log("response: " + params.requestId);
        if (params.requestId == firstid) {
            let decision = 'headers' in params.response;
            // Check download behavior
            decision = decision && ('content-disposition' in params.response.headers 
                            || ('content-type' in params.response.headers && params.response.headers['content-type'].indexOf('octet-stream') != -1));
            // Checkfor content-length (0 means no load event)
            decision = decision || ('Content-Length' in params.response.headers && params.response.headers['Content-Length'] == 0) 
                                || ('content-length' in params.response.headers && params.response.headers['content-length'] == 0)
            if (decision) {
                // console.log("AHA");
                cookieReq.shift();
                if (!cookieReq.length) {
                    client.close();
                    fs.writeFile(path.join('headers', 'compare', filename.replace(/\//g, '_') + '.json'), JSON.stringify(compare), 'utf-8', err => {
                        if (err) throw err;
                    });
                } else {
                    currentUrl = cookieReq[0].url;
                    // console.log("Finished: "+ currentUrl + '\n\n');
                    firstid = 0;
                    turned = false;
                    return Page.navigate({ url: currentUrl });
                }
                return;
            }
            reqheaders[params.requestId] = params.response.requestHeaders;
            // firstid = params.requestId;
            // turned = true;
        }
    });

    Network.loadingFinished(async (params) => {
        //console.log("load: " + params.requestId);
        if (params.requestId == firstid) {
            Page.stopLoading();
            let bytes = 0;
            let data = ''
            try {
                data = await Network.getResponseBody({ requestId: firstid });
                data = data.body;
                bytes = data.length;
            } catch (err) {
            }
            // console.log(bytes);
            if (identical(cookieReq[0], data, resource))
                compare['same'][cookieReq[0].url] = [
                    bytes,
                    cookieReq[0].type,
                    cookieReq[0].initiator
                ];
            else
                compare['diff'][cookieReq[0].url] = {
                    bytes: [bytes, cookieReq[0].bytes, cookieReq[0].type, cookieReq[0].initiator],
                    headers: reqheaders[params.requestId]
                };
            cookieReq.shift();
            if (!cookieReq.length) {
                client.close();
                fs.writeFile(path.join('headers', 'compare', filename.replace(/\//g, '_') + '.json'), JSON.stringify(compare), 'utf-8', err => {
                    if (err) throw err;
                });
            } else {
                currentUrl = cookieReq[0].url;
                // console.log("\n\nFinished: " + currentUrl + '\n\n');
                firstid = 0;
                turned = false;
                return Page.navigate({ url: currentUrl });
            }
        }
    });

    // Page.loadEventFired(() => {
    //     cookieReq.shift();
    //     if (!cookieReq.length) {
    //         client.close();
    //         fs.writeFile(path.join('headers', 'compare', filename + '.json'), JSON.stringify(compare), 'utf-8', err => {
    //             if (err) throw err;
    //         });
    //     } else {
    //         url = cookieReq[0].url;
    //         firstid = 0;
    //         turned = false;
    //         console.log(url);
    //         return Page.navigate({ url: url });
    //     }
    // });

    // enable events then start!
    Promise.all([
        Network.enable(),
        Network.clearBrowserCache(),
        Page.enable(),
        Page.setDownloadBehavior({ behavior: 'deny' })
    ]).then(() =>{
        filename = process.argv[2];
        ReadReq(filename);
        ReadResource(filename);
        currentUrl = cookieReq[0].url;
        return Page.navigate({ url: currentUrl });
    }).catch((err) => {
        console.error(err);
        client.close();
    });

}).on('error', (err) => {
    // cannot connect to the remote endpoint
    console.error(err);
});

