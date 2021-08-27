axios.defaults.xsrfHeaderName = "X-CSRFTOKEN"
axios.defaults.xsrfCookieName = "csrftoken"

function changeAvatar () {
    axios.get('http://127.0.0.1:8000/space/change_avatar', {})
        .then(function (res) {
            if (res.data !== ""){
                console.log(res.data)
                let i = Math.random();
                document.getElementById("Avatar").src=res.data + ".svg?i=" + i;
                document.getElementById("AvatarTiny").src=res.data + ".svg?i=" + i;
            }
            console.log(res)
        })
}