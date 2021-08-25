axios.get('http://127.0.0.1:8000/works/api/stage/1/')
    .then(function (response) {
        // 处理成功情况
        data = response.data
        const editor = new EditorJS({
            autofocus: true,
            data: data
        });

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

function handleSave() {
    editor.save().then((outputData) => {
        console.log('Article data: ', outputData)
    }).catch((error) => {
        console.log('Saving failed: ', error)
    });

}

