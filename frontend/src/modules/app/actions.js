import * as actionTypes from './actionTypes';

export const loading = () => ({
    type: actionTypes.LOADING
});

export const loaded = () => ({
    type: actionTypes.LOADED
});

export const error = error => ({
    type: actionTypes.ERROR,
    error
});

const changeChatCompleted = chat => ({
    type: actionTypes.CHANGE_CHAT,
    chat
})

export const changeChat = (chat) => dispatch => dispatch(changeChatCompleted(chat))

const changeLastChatCompleted = lastChat => ({
    type: actionTypes.CHANGE_LAST_CHAT,
    lastChat
})

export const changeLastChat = (lastChat) => dispatch => dispatch(changeLastChatCompleted(lastChat));
