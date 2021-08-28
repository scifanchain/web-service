import React, {useState, useEffect} from 'react';
import ReactDOM from 'react-dom';
import EditorJS from "@editorjs/editorjs";
import axios from "axios";

import config from "./config"

axios.defaults.xsrfHeaderName = "X-CSRFTOKEN"
axios.defaults.xsrfCookieName = "csrftoken"

export function StageEditor() {
    const [dataStage, setDataStage] = useState({})
    const [method, setMethod] = useState('')
    const [url, setUrl] = useState('')
    const [isReadOnly, setIsReadOnly] = useState(0)

    const [title, setTitle] = useState('')

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
                    data: response.data['content'],
                    readOnly: true,
                    minHeight: 40,
                    onChange: () => {
                        editor.save().then((outputData) => {
                            // setDataStage(outputData)
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
    }, [url, isReadOnly]);

    function handleChange(e) {
        setTitle(e.target.value)
        console.log(title)
    }

    // 验证标题
    function validTitle() {

    }


    const putStage = () => {

    }

    const postStage = () => {
        const putData = {"title": "unity", "content": data, "owner": 1}
        const options = {
            method: 'PUT',
            data: putData,
            url: 'http://127.0.0.1:8000/works/api/stage/1/',
        };
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

    return (
        <div className={"row"}>
            <div className={"col-md-3"}>
                <h6>渐进式的创作</h6>
                <p className="small">你的作品可以在后续不断演化。</p>
            </div>
            <div className={"col-md-8"}>
                <input type="text" className={"form-control mb-2 bg-light"} onChange={handleChange}/>
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

ReactDOM.render(
    <StageEditor/>,
    document.getElementById('stage-wrap')
);