import React from 'react';
import ReactDOM from 'react-dom';
import EditorJS from "@editorjs/editorjs";
import axios from "axios";

import App from './App';

axios.defaults.xsrfHeaderName = "X-CSRFTOKEN"
axios.defaults.xsrfCookieName = "csrftoken"


function StageEditor() {
    const [dataStage, setDataStage] = useState({})
    const [method, setMethod] = useState('')
    const [url, setUrl] = useState('')

    // get stage content
    // url参数锁定该方法在页面不变更只执行一次
    useEffect(() => {
        axios.get('http://127.0.0.1:8000/works/api/stage/1/')
            .then(function (response) {
                // 处理成功情况
                setDataStage(response.data)
                console.log(response);
                const editor = new EditorJS({
                    autofocus: true,
                    holderId: 'stage-editor',
                    data: response.data,
                    readOnly: false,
                    minHeight: 40,
                    tools: {
                        header: {
                            class: Header,
                            inlineToolbar: ['link']
                        },
                        list: {
                            class: List,
                            inlineToolbar: true
                        }
                    },
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


    // save stage data
    const saveStage = () => {
        console.log(data)
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

    const putStage = () => {

    }

    const postStage = () => {

    }

    return (
        <div>
            <div>已保存</div>
            <div id={"menu"} className={"text-end mb-1 pt-2"}>
                <span className={"btn btn-sm px-3 btn-primary mx-3"} onClick={putStage}>保存</span>
                <span className={"btn btn-sm px-3 btn-primary"} onClick={postStage}>提交</span>
            </div>
            <div id={"stage-editor"} className={"border bg-light pt-4"}/>
        </div>
    )
}

ReactDOM.render(
    <StageEditor/>,
    document.getElementById('stage-editor-wrap')
);

ReactDOM.render(
  <React.StrictMode>
    <App />
  </React.StrictMode>,
  document.getElementById('root')
);
