import React from "react";
import ReactDOM from "react-dom";
import { ChangeAvatar, StageEditor, StageView } from './components.js'


const stageEditorWrap = document.getElementById('StageEditorWrap')
const stageViewWrap = document.getElementById('StageViewWrap')
const changeAvatar = document.getElementById('ChangeAvatar')

if (stageEditorWrap) {
    ReactDOM.render(
        <StageEditor/>,
        document.getElementById('StageEditorWrap')
    );
}

if (stageViewWrap) {
    ReactDOM.render(
        <StageView/>,
        document.getElementById('StageViewWrap')
    );
}

if (changeAvatar) {
    ReactDOM.render(
        <ChangeAvatar/> ,
        document.getElementById('ChangeAvatar')
    );
}
