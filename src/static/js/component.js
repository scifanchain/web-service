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


    // get stage content
    // url参数锁定该方法在页面不变更只执行一次
    useEffect(() => {
        axios.get('http://127.0.0.1:8000/api/stages/1/')
            .then(function (response) {
                // 处理成功情况
                setDataStage(response.data)
                console.log(response);
                let k = true;
                if (isReadOnly !== 0){
                    k = false;
                }

                const editor = new EditorJS({
                    autofocus: true,
                    holderId: 'stage-editor',
                    data: response.data['content'],
                    readOnly: k,
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
    }, [url,isReadOnly]);


    const edit = () => {
        setIsReadOnly(1)
        console.log(isReadOnly)
    }

    const edit2 = () =>{
        setIsReadOnly(2)
        console.log(isReadOnly)
    }

    // save stage data
    const saveStage = () => {
        console.log(data)

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
        <div>
            <div>已保存</div>
            <div id={"menu"} className={"text-end mb-1 pt-2"}>
                <span className={"btn btn-sm px-3 btn-primary mx-3"} onClick={edit}>保存</span>
                <span className={"btn btn-sm px-3 btn-primary"} onClick={edit2}>提交</span>
            </div>
            <div id={"stage-editor"}/>
        </div>
    )
}

ReactDOM.render(
    <StageEditor/>,
    document.getElementById('stage-editor-wrap')
);