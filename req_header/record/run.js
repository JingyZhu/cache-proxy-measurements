const CDP = require('chrome-remote-interface');
const fs = require('fs')
const parse = require('url').parse
const path = require('path')

const lease = 24 * 60 * 60;

let method = {};
let type = {};
let postData = {};

let cacheable = {}; // requestId: {headers: requestHeaders object, url: url}
let uncacheable = {};

function extractNum(str, pos) {
    for (var i = pos; i < str.length; i++) {
        if (str[i] < '0' || str[i] > '9') break;
    }
    return parseInt(str.substring(pos, i));
}

CDP({ port: process.argv[3] }, (client) => {
    // extract domains
    const { Network, Page, Security } = client;
    // console.log(Security);

    Security.setIgnoreCertificateErrors({ ignore: true });
    //Security.disable();

    Network.requestWillBeSent((params) => {
        method[params.requestId] = params.request.method;
        type[params.requestId] = params.type;
        if (params.request.hasPostData && params.request.postData)
            postData[params.requestId] = params.request.postData;
    });

    // setup handlers
    Network.responseReceived((params) => {
        const cacheControl1 = params.response.headers['cache-control'];
        const cacheControl2 = params.response.headers['Cache-Control'];
        // console.log(`*\t${cacheControl1}\t${cacheControl2}`);
        let cacheControl = null;
        if (cacheControl1 != null) {
            cacheControl = cacheControl1;
        } else if (cacheControl2 != null) {
            cacheControl = cacheControl2;
        }
        if (cacheControl != null) {
            const private = cacheControl.indexOf("private");
            const maxage = cacheControl.indexOf("max-age=");
            let bdigit = 0;
            if (maxage > -1) {
                bdigit = extractNum(cacheControl, maxage + 8);
            }
            if (bdigit > 0 && private == -1) { // This request is cacheable
                cacheable[params.requestId] = {
                    'url': params.response.url,
                    'method': method[params.requestId],
                    'type': type[params.requestId],
                    'headers': params.response.requestHeaders,
                    'response': params.response.headers
                };
                if (params.requestId in postData)
                    cacheable[params.requestId]['postData'] = postData[params.requestId];
            }
        }
        else {
            uncacheable[params.requestId] = {
                'url': params.response.url,
                'method': method[params.requestId],
                'type': type[params.requestId],
                'headers': params.response.requestHeaders,
                'postData': postData[params.requestId],
                'response': params.response.headers
            };
            if (params.requestId in postData)
                uncacheable[params.requestId]['postData'] = postData[params.requestId];
        }
    });

    Network.loadingFinished(params => {
        if (params.requestId in cacheable)
            cacheable[params.requestId]['bytes'] = params.encodedDataLength;
        else if (params.requestId in uncacheable)
            uncacheable[params.requestId]['bytes'] = params.encodedDataLength;
    });

    Page.loadEventFired(() => {
        client.close();
        fs.writeFile(path.join('..', 'headers', 'cacheable', parse(process.argv[2]).host + '.json'), JSON.stringify(cacheable), 'utf-8', err => {
            if (err) throw err;
        });
        fs.writeFile(path.join('..', 'headers', 'uncacheable', parse(process.argv[2]).host + '.json'), JSON.stringify(uncacheable), 'utf-8', err => {
            if (err) throw err;
        });
    });

    // enable events then start!
    Promise.all([
        Network.enable(),
        Page.enable()
    ]).then(() => {
        return Page.navigate({ url: process.argv[2] });
    }).catch((err) => {
        console.error(err);
        client.close();
    });

}).on('error', (err) => {
    // cannot connect to the remote endpoint
    console.error(err);
});
