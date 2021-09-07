import axios from "axios";

axios.defaults.xsrfHeaderName = "X-CSRFTOKEN"
axios.defaults.xsrfCookieName = "csrftoken"

import config from './config'


const changeAvatar = () => {
    axios.get(config.API_URL + 'space/change_avatar')
        .then(function (res) {
            if (res.data !== "") {
                console.log(res.data)
                let i = Math.random();
                document.getElementById("Avatar").src = res.data + ".svg?i=" + i;
                document.getElementById("AvatarTiny").src = res.data + ".svg?i=" + i;
            }
        })
}
