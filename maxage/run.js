const CDP = require('chrome-remote-interface');

const lease = 24 * 60 * 60;

function extractNum(str, pos) {
    for (var i = pos; i < str.length; i++) {
        if (str[i] < '0' || str[i] > '9') break;
    }
    return parseInt(str.substring(pos, i));
}

CDP((client) => {
    // extract domains
    const { Network, Page, Security } = client;
    // console.log(Security);

    Security.setIgnoreCertificateErrors({ ignore: true });
    //Security.disable();

    Network.setUserAgentOverride({userAgent: "Mozilla/5.0 (Linux; <Android Version>; <Build Tag etc.>) AppleWebKit/<WebKit Rev> (KHTML, like Gecko) Chrome/<Chrome Rev> Mobile Safari/<WebKit Rev>"});
    
    // setup handlers
    Network.responseReceived((params) => {
        console.log(`1\t${params.requestId}\t${params.response.url}`);
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
            if (bdigit > 0 && private == -1) {
                console.log(`2\t${params.requestId}\t${bdigit}`);
            }
        }
    });

    Network.loadingFinished((params) => {
        console.log(`3\t${params.requestId}\t${params.encodedDataLength}`);
    });
    Page.loadEventFired(() => {
        client.close();
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
