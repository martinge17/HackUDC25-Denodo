const getModuleState = state => state.app;

export const getError = state => getModuleState(state).error;

export const isLoading = state => getModuleState(state).loading;

export const getChat = state => getModuleState(state).chat;

export const getLastChat = state => getModuleState(state).lastChat;

export const menu = state => getModuleState(state).menu;