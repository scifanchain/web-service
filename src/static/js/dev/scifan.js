axios.defaults.xsrfHeaderName = "X-CSRFTOKEN"
axios.defaults.xsrfCookieName = "csrftoken"

import config from '../config'

function changeAvatar() {
    axios.get(config.api.uri + 'space/change_avatar')
        .then(function (res) {
            if (res.data !== "") {
                console.log(res.data)
                let i = Math.random();
                document.getElementById("Avatar").src = res.data + ".svg?i=" + i;
                document.getElementById("AvatarTiny").src = res.data + ".svg?i=" + i;
            }
        })
}