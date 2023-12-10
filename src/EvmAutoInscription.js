/**
 * 批量打evm的铭文，极度的简单，最主要的三要素
 * 1、节点地址
 * 2、钱包私钥
 * 3、铭文json
 * 
 * 通俗来说，evm的铭文，就是给自己发送一段hex即可，所以抽象来看，打铭文就是给自己执行一段0转交易
 */
const ethers = require('ethers');


// 铭文的json格式，如：data:,{"p":"xrc-20","op":"mint","tick":"okts","amt":"1000"}
const inscriptionJson = '';

// 钱包私钥，支持多个钱包打
const privateKeys = [
    '私钥1',
    '私钥2'
];

// 节点地址，支持多个节点打，防止单个节点被封
const providers = [
    new ethers.JsonRpcProvider('节点 url1'),
    new ethers.JsonRpcProvider('节点 url2')
];

// 限制操作，如限制打的数量
const inscrlimt = 10;


// ------------------------------ 以下函数方法 ------------------------------


const strToHex = (str) => {
    return '0x' + Buffer.from(str, 'utf8').toString('hex');
}

const task = async (pk, i) => {
    // 1、获取提供者
    let provider = providers[i % providers.length];
    // 2、通过私钥链接账户
    let account = new ethers.Wallet(pk, provider);
    // 3、构建发送参数
    let nonce = await account.getNonce();
    let add = await account.getAddress();
    for (let j = 0; j < inscrlimt; j++) {
        let sendOptions = {
            to: add,
            value: 0,
            data: strToHex(inscriptionJson),
            nonce: nonce++
        };
        // 4、发送交易
        const rep = await account.sendTransaction(sendOptions);
        console.log(rep);
    }
};

function main() {
    for (let i = 0; i < privateKeys.length; i++) {
        task(privateKeys[i], i);
    }
}

main();
