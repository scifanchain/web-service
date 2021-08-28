import EditorJS from "@editorjs/editorjs";
import axios from "axios";

axios.defaults.xsrfHeaderName = "X-CSRFTOKEN"
axios.defaults.xsrfCookieName = "csrftoken"


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