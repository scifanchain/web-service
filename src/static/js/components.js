import React, {useState, useEffect, useRef} from 'react';
import ReactDOM from 'react-dom';
import EditorJS from "@editorjs/editorjs";
import axios from "axios";

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
                data: {"title": title, "content": dataStage, "owner": userId},
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
                data: {"title": title, "content": dataStage, "owner": userId},
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
                <input type="text" className={"form-control mb-2 bg-light"} onChange={handleChange} onBlur={ checkTitle }/>
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
                        <i className="bi-file-arrow-up-fill me-1"/>
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
    const stageId = document.getElementById("StageViewWrap").getAttribute("data-stageId")
    console.log(stageId)
    useEffect(() => {
        axios.get(config.API_URL + 'stages/' + stageId + '/')
            .then(function (response) {
                console.log(response);
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
        <div id={"stageView"}></div>
    )
}

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