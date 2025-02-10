import {Route, Routes, useLocation} from "react-router-dom";
import {paths} from "../../utils/constants";
import AppRoute from "../app-route/AppRoute";
import HomePage from "../../pages/HomePage";
import SetsPage from "../../pages/SetsPage";

export default function App() {
    const location = useLocation();
    const background = location.state && location.state.background;

    return (
        <>
            <Routes location={background || location}>
                <Route path={paths.DEFAULT} element={
                    <AppRoute isProtected={false}>
                        <HomePage/>
                    </AppRoute>
                }/>
                <Route path={paths.SETS} element={
                    <AppRoute isProtected={true}>
                        <SetsPage/>
                    </AppRoute>
                }/>
            </Routes>
        </>
    )
}