import axios from "axios";
import React, {useState, useEffect} from 'react';
import ReactDOM from 'react-dom'

axios.defaults.xsrfHeaderName = "X-CSRFTOKEN"
axios.defaults.xsrfCookieName = "csrftoken"

import config from './config'


function changeAvatar() {
    axios.get(config.API_URL + 'authors/change_avatar')
        .then(function (res) {
            if (res.data !== "") {
                console.log(res.data)
                let i = Math.random();
                document.getElementById("Avatar").src = res.data + ".svg?i=" + i;
                document.getElementById("AvatarTiny").src = res.data + ".svg?i=" + i;
            }
        })
}
