import React from "react";
import ReactDOM from "react-dom";
import { StageEditor, StageView } from './components.js'


const stageEditorWrap = document.getElementById('StageEditorWrap')
const stageViewWrap = document.getElementById('StageViewWrap')

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
