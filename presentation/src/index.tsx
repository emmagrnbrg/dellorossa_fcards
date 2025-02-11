import React from 'react';
import ReactDOM from 'react-dom/client';
import './index.css';
import {BrowserRouter, Route, Routes} from "react-router-dom"
import App from "./components/app/App";
import {applyMiddleware, compose} from "redux";
import {rootReducer} from "./services/reducers";
import {Provider} from "react-redux";
import {configureStore, Tuple} from "@reduxjs/toolkit";
import {thunk} from "redux-thunk";

const root = ReactDOM.createRoot(document.getElementById("root") as HTMLElement);

declare global {
    interface Window {
        __REDUX_DEVTOOLS_EXTENSION_COMPOSE__?: typeof compose;
    }
}

const composeEnhancers = window.__REDUX_DEVTOOLS_EXTENSION_COMPOSE__ || compose;
export const store = configureStore({
    reducer: rootReducer,
    enhancers: () => new Tuple(composeEnhancers(applyMiddleware(thunk)))
});

root.render(
    <React.StrictMode>
        <Provider store={store}>
            <BrowserRouter>
                <Routes>
                    <Route path="*" element={ <App /> }/>
                </Routes>
            </BrowserRouter>
        </Provider>
    </React.StrictMode>
);
