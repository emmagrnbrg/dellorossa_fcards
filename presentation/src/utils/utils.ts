import {storageKeys} from "./constants";

export const updateTokens = (response: {refreshToken: string, accessToken: string}) => {
    localStorage.setItem(storageKeys.REFRESH_TOKEN, response.refreshToken);
    localStorage.setItem(storageKeys.ACCESS_TOKEN, response.accessToken);
}

export const isAuth = (): boolean => localStorage.refreshToken;