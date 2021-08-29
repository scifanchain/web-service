import React, {useState, useEffect, useRef} from 'react';
import ReactDOM from 'react-dom';
import EditorJS from "@editorjs/editorjs";
import axios from "axios";

import config from "./config"

axios.defaults.xsrfHeaderName = "X-CSRFTOKEN"
axios.defaults.xsrfCookieName = "csrftoken"

export function StageEditor() {
    const userId = document.getElementById('StageWrap').getAttribute('data-userId')
    const [dataStage, setDataStage] = useState({})
    const [method, setMethod] = useState('')
    const [url, setUrl] = useState('')
    const [title, setTitle] = useState('')
    const [titleError, setTitleError] = useState('')

    // get stage content
    // url参数锁定该方法在页面不变更只执行一次
    useEffect(() => {


        axios.get(config.API_URL + 'stages/1/')
            .then(function (response) {
                // 处理成功情况
                setDataStage(response.data)
                console.log(response);

                const editor = new EditorJS({
                    autofocus: true,
                    holder: 'stage-editor',
                    data: dataStage,
                    readOnly: false,
                    minHeight: 40,
                    onChange: () => {
                        editor.save().then((outputData) => {
                            setDataStage(outputData)
                            console.log(outputData);
                        }).catch
                        ((error) => {
                            console.log('Saving failed: ', error)
                        });
                    }
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
    }, [url]);

    // 标题值改变
    // todo: 验证是否有重名标题，有的话给出提示
    function handleChange(e) {
        setTitle(e.target.value)
        if (title.length >= 1) {
            setTitleError('')
        }
        console.log(title)
    }

    // 验证标题是否为空
    function titleValidated() {
        if (title.length < 1) {
            setTitleError("标题不能为空")
            return false
        } else {
            setTitleError('')
        }
        return true
    }

    function submitStage(options) {
        axios(options)
            .then(function (response) {
                if (method === 'post') {
                    window.location.reload();
                }
                console.log(response);
            })
            .catch(function (error) {
                console.log(error);
            });
    }

    // 保存
    const putStage = () => {
        titleValidated()
    }

    // 提交
    const postStage = () => {
        if (titleValidated()) {
            const options = {
                method: 'post',
                data: {"title": title, "content": dataStage, "owner": userId},
                url: config.API_URL + 'stages/',
            };
            submitStage(options);
            window.location.href = "/space/works/";
        }
    }

    return (
        <div className={"row"}>
            <div className={"col-md-3"}>
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
                <input type="text" className={"form-control mb-2 bg-light"} onChange={handleChange}/>
                {titleError !== '' &&
                <p className={"bg-danger"}>{titleError}</p>
                }
                <div className={"stage-editor-wrap bg-light"}>
                    <div className={"border rounded"} id={"stage-editor"}></div>
                </div>
            </div>
            <div className={"col-md-1"}>
                <div className="sticky-top">
                    <a className="btn btn-small btn-primary px-2 mb-2" onClick={putStage}>
                        <i className="bi-file-earmark-check-fill me-1"></i>
                        <span className="small">保存</span>
                    </a>
                    <a className="btn btn-small btn-primary px-2 mb-2" onClick={postStage}>
                        <i className="bi-file-arrow-up-fill me-1"/>
                        <span className="small">提交</span>
                    </a>
                </div>
            </div>
        </div>
    )
}


export function StageView() {
    useEffect(() => {
        axios.get(config.API_URL + 'stages/1/')
            .then(function (response) {
                // 处理成功情况
                setDataStage(response.data)
                console.log(response);

                const editor = new EditorJS({
                    autofocus: true,
                    holder: 'stage-editor',
                    data: dataStage,
                    readOnly: false,
                    minHeight: 40,
                    onChange: () => {
                        editor.save().then((outputData) => {
                            setDataStage(outputData)
                            console.log(outputData);
                        }).catch
                        ((error) => {
                            console.log('Saving failed: ', error)
                        });
                    }
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
    }, [url]);

    return (
        <div>gooddgdsgdsgdsgsdgsd</div>
    )
}