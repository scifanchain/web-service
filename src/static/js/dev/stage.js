axios.defaults.xsrfHeaderName = "X-CSRFTOKEN"
axios.defaults.xsrfCookieName = "csrftoken"

function createEditor() {
    const data = {}
    const editor = new EditorJS({
        autofocus: true,
        holder: 'stage-editor',
        readOnly: false,
        minHeight: 40,
        onChange: () => {
            editor.save().then((outputData) => {
                console.log(outputData.blocks);
            }).catch
            ((error) => {
                console.log('Saving failed: ', error)
            });
        }
    });
}


function getStage() {
    axios.get('http://127.0.0.1:8000/works/api/stage/1/')
        .then(function (response) {
            // 处理成功情况
            console.log(response);
            const editor = new EditorJS({
                autofocus: true,
                holder: 'stage-editor',
                data: response.data,
                readOnly: false,
                minHeight: 40,
                onChange: () => {
                    editor.save().then((outputData) => {
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
}