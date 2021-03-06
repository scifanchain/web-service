import React from "react";
import ReactDOM from "react-dom";
import { ChangeAvatar, StageEditor, StageView, CreateWallet, Wallet } from './components.js'

const stageEditorWrap = document.getElementById('StageEditorWrap')
const stageViewWrap = document.getElementById('StageViewWrap')
const changeAvatar = document.getElementById('ChangeAvatar')
const createWalletButton = document.getElementById('CreateWalletButton')
const walletWrap = document.getElementById('WalletWrap')


if (stageEditorWrap) {
    ReactDOM.render(
        <StageEditor />,
        document.getElementById('StageEditorWrap')
    );
}

if (stageViewWrap) {
    ReactDOM.render(
        <StageView />,
        document.getElementById('StageViewWrap')
    );
}

if (changeAvatar) {
    ReactDOM.render(
        <ChangeAvatar />,
        document.getElementById('ChangeAvatar')
    );
}

if (createWalletButton) {
    ReactDOM.render(
        <CreateWallet />,
        document.getElementById('CreateWalletButton')
    );
}

if (walletWrap) {
    ReactDOM.render(
        <Wallet />,
        document.getElementById('WalletWrap')
    );
}