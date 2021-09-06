import {StageEditor, StageView} from './components/stage'
import ReactDOM from "react-dom";
import React from "react";

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
