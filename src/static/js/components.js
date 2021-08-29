import React, {useState, useEffect, useRef} from 'react';
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
    const [title, setTitle] = useState('')

    const allow_title = useRef(false)

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

    function handleChange(e) {
        setTitle(e.target.value)
        console.log(title)
    }

    // 验证标题
    function validTitle() {
        if (title.length > 1) {
            allow_title.current = true
        }
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
                {allow_title &&
                <p className={"bg-danger"} id={"titleError"}>请输入标题</p>
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

ReactDOM.render(
    <StageEditor/>,
    document.getElementById('stage-wrap')
);