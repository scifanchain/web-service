axios.defaults.xsrfHeaderName = "X-CSRFTOKEN"
axios.defaults.xsrfCookieName = "csrftoken"

import config from '../config'

const editor = new EditorJS({
    autofocus: true,
    holder: 'stage-editor',
    readOnly: false,
    minHeight: 241,
});

function submitStage() {
    // 验证标题

    editor.isReady.then(() => {
        editor.save().then((outputData) => {
            console.log('Article data: ', outputData)
            const putData = {"title": "unity", "content": outputData, "owner": 1}
            axios.post(config.api.url + 'stages/', putData)
                .then(function (response) {
                    // 处理成功情况
                    // 返回创作空间作品列表页面
                    window.location= '/space/works/';
                    console.log(response);
                })
                .catch(function (error) {
                    // 处理错误情况
                    console.log(error);
                })
                .then(function () {
                    // 总是会执行
                    console.log("OK!")
                });
        }).catch((error) => {
            console.log('Saving failed: ', error)
        });
    })
}

function saveStage() {
    editor.isReady.then(() => {
        editor.save().then((outputData) => {
            console.log('Article data: ', outputData)
            editor.readOnly.toggle();
            const putData = {"title": "unity", "content": outputData, "owner": 1}
            axios.put('http://127.0.0.1:8000/api/stages/', putData)
                .then(function (response) {
                    // 处理成功情况
                    console.log(response);
                })
                .catch(function (error) {
                    // 处理错误情况
                    console.log(error);
                })
                .then(function () {
                    // 总是会执行
                    console.log("OK!")
                });
        }).catch((error) => {
            console.log('Saving failed: ', error)
        });
    })
}

function editStage(){
    editor.isReady.then(() => {
        editor.readOnly.toggle();
    })
}
