import React, { useState, useEffect, useRef } from 'react';
import EditorJS from "@editorjs/editorjs";
import axios from "axios";

import { ApiPromise, WsProvider } from '@polkadot/api';
import { stringToU8a, u8aToHex } from '@polkadot/util';
import { signatureVerify, mnemonicGenerate } from '@polkadot/util-crypto';
import { Keyring } from '@polkadot/keyring';

import config from "./config"

axios.defaults.xsrfHeaderName = "X-CSRFTOKEN"
axios.defaults.xsrfCookieName = "csrftoken"


// Stage编辑组件
export function StageEditor() {
    const userId = document.getElementById('StageEditorWrap').getAttribute('data-userId')
    const stageId = document.getElementById('StageEditorWrap').getAttribute('data-stageId')

    const [dataStage, setDataStage] = useState({})
    const [method, setMethod] = useState('')
    const [url, setUrl] = useState('')
    const [title, setTitle] = useState('')
    const [titleError, setTitleError] = useState('')
    const [contentError, setContentError] = useState('')
    const [titleEnable, setTitleEnable] = useState(false)

    // get stage content
    // url参数锁定该方法在页面不变更只执行一次
    useEffect(() => {
        if (stageId) { // 编辑页面才会传入stageId
            axios.get('http://127.0.0.1:8000/api/stages/23/').then(function (res) {
                initEditor(res.data['content'])
                console.log(res.data['content']);
            })
        } else { // 新创建页面，初始化数据dataStage没有值
            initEditor(dataStage);
        }

        // 初始化编加器
        function initEditor(data) {
            const editor = new EditorJS({
                // autofocus: true,
                holder: 'StageEditor',
                data: data,
                readOnly: false,
                minHeight: 120,
                onChange: () => {
                    editor.save().then((outputData) => {
                        setDataStage(outputData)
                    }).catch
                        ((error) => {
                            console.log('Saving failed: ', error)
                        });
                }
            });
        }
    }, [url]);

    // 标题值改变
    function handleChange(e) {
        setTitle(e.target.value)
        if (title.length >= 1) {
            setTitleError('')
        }
        console.log(title)
    }

    // 标题是否重名
    function checkTitle(e) {
        axios.post('/works/check_title', {
            'title': e.target.value
        }).then(function (res) {
            if (res.data == 'no') {
                setTitleEnable(false)
                setTitleError("这个标题已经有人用了，请修改后再次提交。")
            } else {
                setTitleEnable(true)
            }
        })
    }

    // 验证标题
    function titleValidated() {
        if (title.length < 1) {
            setTitleError("请为作品设置标题。")
            return false
        }
        if (titleEnable == false) {
            return false
        }
        return true
    }

    function contentValidated() {
        console.log(dataStage);
        if (dataStage.blocks.length < 1) {
            setContentError("内容为空。如果你是从别的地方复制过来的内容，请在编辑器中做些修改，这样编辑器才能获取到内容。")
            return false
        }
        return true
    }

    function submitStage(options) {
        axios(options)
            .then(function (response) {
                console.log(response);
            })
            .catch(function (error) {
                console.log(error);
            });
    }

    // 保存
    const putStage = () => {
        if (titleValidated() && contentValidated()) {
            const options = {
                method: 'put',
                data: { "title": title, "content": dataStage, "owner": userId },
                url: config.API_URL + 'stages/' + userId,
            };
            submitStage(options);
            window.location.href = "/space/works/";
        }
    }

    // 提交
    const postStage = () => {
        if (titleValidated() && contentValidated()) {
            const options = {
                method: 'post',
                data: { "title": title, "content": dataStage, "owner": userId },
                url: config.API_URL + 'stages/',
            };
            submitStage(options);
            window.location.href = "/space/works/";
        }
    }

    return (
        <div className={"row"}>
            <div className={"col-md-2"}>
                <h6>渐进式的创作</h6>
                <p className="small">你的作品可以在后续不断演化。</p>
                <table className="table caption-top">
                    <caption>List of users</caption>
                    <thead>
                        <tr>
                            <td>字数</td>
                            <td>Token</td>
                        </tr>
                    </thead>
                    <tbody>
                        <tr>
                            <td>5051</td>
                            <td>50</td>
                        </tr>
                    </tbody>
                </table>
                <h5>内容元素</h5>
                人物
            </div>
            <div className={"col-md-8"}>
                <input type="text" className={"form-control mb-2 bg-light"} onChange={handleChange} onBlur={checkTitle} />
                {titleError !== '' &&
                    <p className={"bg-warning bg-opacity-25 p-2 rounded text-danger"}>{titleError}</p>
                }
                {contentError !== '' &&
                    <p className={"bg-danger"}>{contentError}</p>
                }
                <div className={"stage-editor-wrap"}>
                    <div className={"rounded p-4 border bg-light"} id={"StageEditor"}></div>
                </div>
            </div>
            <div className={"col-md-2"}>
                <div className="sticky-top">
                    <button className="btn btn-small btn-primary px-5 mb-2" onClick={postStage}>
                        <i className="bi-file-arrow-up-fill me-1" />
                        <span className="small">提交</span>
                    </button>
                    <br />
                    <a className="p3-2 mb-2" onClick={putStage}>
                        <i className="bi-file-earmark-check-fill me-1"></i>
                        <span className="small">保存</span>
                    </a>
                    <br />

                </div>
            </div>
        </div>
    )
}

// stage显示组件
export function StageView() {
    // Substrate connection config
    const WEB_SOCKET = config.WEB_SOCKET;

    const connectSubstrate = async () => {
        const wsProvider = new WsProvider(WEB_SOCKET);
        const api = await ApiPromise.create({ provider: wsProvider, types: {} });
        return api;
    };

    // This is 1 Unit
    const TX_AMT = 1000000000000000;

    // state
    const [dataStage, setDataStage] = useState({})
    const [stageHash, setStageHash] = useState('')
    const [stageOwner, setStageOwner] = useState('')
    const [blockNum, setBlockNum] = useState('')

    const stageId = document.getElementById("StageViewWrap").getAttribute("data-stageId")

    async function verifyStage() {
        const api = await connectSubstrate();
        const keyring = new Keyring({ type: 'ed25519' });
        // just for dev
        const alice = keyring.addFromUri('//Alice');

        signature = alice.sign(stringToU8a(dataStage))
        setStageHash(u8aToHex(signature))

        // const { isValid } = signatureVerify(message, signature, alice.address);

        await api.query.poe
            .proofs(hashstr, (result) => {
                // poe storage item returns a tuple, which is represented as an array.
                setStageOwner(result[0].toString());
                setBlockNum(result[1].toNumber());
                console.log(result[0].toString())
                console.log(result[1].toNumber())
            })
            .then(() => {
                console.log('this is end.');
            });
    }

    async function poeStage() {
        const api = await connectSubstrate();
        const keyring = new Keyring({ type: 'sr25519' });
        const alice = keyring.addFromUri('//Alice');

        const txResHandler = ({ status }) =>
            status.isFinalized
                ? console.log(`😉 Finalized. Block hash: ${status.asFinalized.toString()}`)
                : console.log(`Current transaction status: ${status.type}`);

        const txErrHandler = err =>
            console.log(err);

        const poe = await api.tx.poe.createProof(stageHash).signAndSend(alice, txResHandler)
            .catch(txErrHandler);
        console.log("poe:" + poe)
    }

    useEffect(() => {
        axios.get(config.API_URL + 'stages/' + stageId + '/')
            .then(function (response) {
                console.log(response.data);
                setDataStage(response.data)
                const editor = new EditorJS({
                    autofocus: false,
                    holder: 'stageView',
                    data: response.data['content'],
                    readOnly: true,
                    minHeight: 120,
                });
            })
            .catch(function (error) {
                // 处理错误情况
                console.log(error);
            })
            .then(function () {
                // 总是会执行
                console.log("OK!")
            });
    }, []);

    return (
        <div>
            <div>
                <button className={'btn btn-primary btn-sm mx-2'} onClick={verifyStage}>验证Hash</button>
                <button className={'btn btn-primary btn-sm mx-2'} onClick={poeStage}>上链存证</button>
            </div>
            {stageHash !== '' &&
                <div>{u8aToHex(stageHash)}</div>
            }

            <div id={"stageView"}></div>
        </div>
    )
}


// 修改头像
export function ChangeAvatar() {

    const changeAvatar = () => {
        axios.get(config.URL + 'space/change_avatar/')
            .then(function (res) {
                if (res.data !== "") {
                    console.log(res.data)
                    let i = Math.random();
                    document.getElementById("Avatar").src = res.data + ".svg?i=" + i;
                    document.getElementById("AvatarTiny").src = res.data + ".svg?i=" + i;
                }
            })
    }

    return (
        <div className={"text-center"}>
            <span className={"btn btn-sm btn-light"} onClick={changeAvatar}>换个随机头像</span>
        </div>
    )
}

// 生成钱包
export function CreateWallet() {

    const [mnemonicWrods, setMnemonicWords] = useState('')
    const [address, setAddress] = useState('')
    const [publickey, setPublickey] = useState('')

    function makeMnemonic() {
        const mnemonic = mnemonicGenerate();
        setMnemonicWords(mnemonic)
        console.log(mnemonic)
    }

    async function makeWallet() {
        // Substrate connection config
        const WEB_SOCKET = config.WEB_SOCKET;

        const connectSubstrate = async () => {
            const wsProvider = new WsProvider(WEB_SOCKET);
            const api = await ApiPromise.create({ provider: wsProvider, types: {} });
            return api;
        };

        const api = await connectSubstrate();
        const keyring = new Keyring();

        // create & add the pair to the keyring with the type and some additional
        // metadata specified
        const pair = keyring.addFromUri(mnemonicWrods, { name: 'first pair' }, 'ed25519');

        axios.post(config.URL + 'space/create_wallet/', {
            address: pair.address,
            publickey: u8aToHex(pair.publicKey)
        }).then(function (res) {
            if (res.data.code == 0) {
                setAddress(pair.address)
                setPublickey(u8aToHex(pair.publicKey))
            } else {
                console.log(res.data.msg)
            }
            console.log(res)
        })

        // the pair has been added to our keyring
        console.log(keyring.pairs.length, 'pairs available');

        // log the name & address (the latter encoded with the ss58Format)
        console.log(pair.meta.name, 'has address', pair.address);
        console.log(pair.meta.name, 'has public_key', u8aToHex(pair.publicKey));
    }

    return (
        <div>
            <p>在区块链中，钱包是一个基本工具，拥有钱包才能获取SFT资产，进行交易、参与社区治理等。</p>
            <button className={"btn btn-danger"} onClick={makeMnemonic}>生成钱包</button>
            {mnemonicWrods !== '' &&
                <div className={'py-3'}>
                    <h2>助记词</h2>
                    <h4 className={'bg-success bg-opacity-10 p-3 border text-danger'}>{mnemonicWrods}</h4>
                    <p>助记词只是私钥的另一种展现形式。由12个英文单词组成。如果由于某种原因造成钱包丢失，只要你记住这些单词，按照顺序在钱包中输入，就能恢复钱包并且进行任意操作。如果别人拿到了你的助记词，就相当于拿到了你的私钥，对你的资产进行掌控。</p>
                    <p>所以以上助记词对您的钱包非常重要！为了安全起见，它只在生成时出现一次，所以请<span className={'text-danger fw-bold'}>现在立即</span>将上面的助记词用纸笔记下来或打印。</p>
                    <p>在存储私钥、助记词时，我们都建议采用离线形式（手抄、打印等）进行数据备份，同时将备份好的内容妥善保管。我们不建议您进行截屏、网络传输（QQ、微信）、云端存储等方式备份，这些方式都有可能遭遇攻击，从而造成资产损失。</p>
                    <p>当您确保记录好助记词之后，再点以下按钮继续操作。</p>
                    <button className={'btn btn-success'} onClick={makeWallet}>继续</button>
                </div>

            }
        </div>
    )
}

export function Wallet() {

    const WEB_SOCKET = config.WEB_SOCKET;
    const wsProvider = new WsProvider(WEB_SOCKET);
    const WEE = "5GrwvaEF5zXb26Fz9rcQpDWS57CtERHpNehXCPcNo";

    useEffect(async () => {
        const api = await ApiPromise.create({ provider: wsProvider, types: {} });
        console.log(api.genesisHash.toHex());
        console.log(api.rpc.state.getMetadata());
        console.log(api.derive.chain.bestNumber);
    })
    
    return (
        <div>你拥有的SFT：</div>
    )
}