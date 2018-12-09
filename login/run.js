/*
Load the page the record the resources / reqresp
*/
const CDP = require('chrome-remote-interface');
const fs = require('fs')
const parse = require('url').parse
const path = require('path')

let method = {};
let type = {};
let postData = {};


let reqStat = {'available': {}, 'unavailable': {}};
let initiator = {};
let resources = {};


function extractNum(str, pos) {
    for (var i = pos; i < str.length; i++) {
        if (str[i] < '0' || str[i] > '9') break;
    }
    return parseInt(str.substring(pos, i));
}

function getFileName(){
    let index = '';
    if (process.argv.length > 3) 
        index = process.argv[3];
    let pathname = '';
    if ( parse(process.argv[2]).pathname != '/')
        pathname =  parse(process.argv[2]).pathname;
    if (index != '') index = '.' + index
    const filename = (parse(process.argv[2]).host + pathname).replace(/\//g, '_') + index + '.json';
    return filename;
} 

function sizeofObj(obj){
    let len = 0;
    for (let key in obj)
        len += key.length + obj.key.length;
    return len;
}

async function newtab(){
    const target = await CDP.New();
    return target
}

async function main(){
    const target = await newtab();

    CDP({target: target.id}, (client) => {
        
        const { Network, Page, Security, Target } = client;
        // console.log(Security);
        Security.setIgnoreCertificateErrors({ ignore: true });
        //Security.disable();

        Network.requestWillBeSent((params) => {
            let initiator_url = null;
            if ('url' in params.initiator){
                //console.log(params.initiator.type, " ", params.initiator.url);
                initiator_url = params.initiator.url;
            }
            else if ('stack' in params.initiator && 'callFrames' in params.initiator.stack){
                initiator_url = params.initiator.stack.callFrames[0].url;
            }
            else
                initiator_url = 'nothing'
            method[params.requestId] = params.request.method;
            type[params.requestId] = params.type;
            initiator[params.requestId] = initiator_url;
            if (params.request.hasPostData && params.request.postData)
                postData[params.requestId] = params.request.postData;
        });

        // setup handlers
        Network.responseReceived((params) => {
            reqStat['available'][params.requestId] = {
                'url': params.response.url,
                'method': method[params.requestId],
                'type': type[params.requestId],
                'headers': params.response.requestHeaders,
                'response': params.response.headers,
                'initiator': initiator[params.requestId]
            };
        });

        Network.loadingFinished(params => {
            const url = reqStat['available'][params.requestId]['url']
            reqStat['available'][params.requestId]['bytes'] = params.encodedDataLength
            Network.getResponseBody({requestId: params.requestId})
            .then( data => {
                reqStat['available'][params.requestId]['length'] = data.body.length;
                resources[url] = {
                        "body": data.body,
                        "type": reqStat['available'][params.requestId]['type']
                }
            }).catch(() => {
                reqStat['available'][params.requestId]['length'] = 0;
                resources[url] = {
                    "body": '',
                    "type": reqStat['available'][params.requestId]['type']
                };
            });
            // reqStat[params.requestId]['bytes'] = Network.getResponseBody(params.requestId).length;
        });

        Page.loadEventFired(async () => {
            client.close();
            for (let key in reqStat['available']){
                if(!('length' in reqStat['available'][key]) || reqStat['available'][key]['length'] == null || reqStat['available'][key]['length'] == undefined){
                    delete reqStat['available'].key;
                }
            }
            const filename = getFileName();
            fs.writeFile(path.join('headers', 'meta', filename), JSON.stringify(reqStat), 'utf-8', err => {
                if (err) throw err;
            });
            fs.writeFile(path.join('headers', 'resources', filename), JSON.stringify(resources), 'utf-8', err=>{
                if (err) throw err;
            });
            CDP.Close({id: target.id});
        });

        // enable events then start!
        Promise.all([
            Network.enable(),
            Page.enable()
        ]).then(() => {
            Network.clearBrowserCache();
            return Page.navigate({ url: process.argv[2] });
        }).catch((err) => {
            console.error(err);
            client.close();
        });

    }).on('error', (err) => {
        // cannot connect to the remote endpoint
        console.error(err);
    });
}

main();
