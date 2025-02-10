import {Navigate, useLocation} from "react-router-dom";
import {isAuth} from "../../utils/utils";
import {PropsWithChildren} from "react";
import {paths} from "../../utils/constants";

export default function AppRoute(props: PropsWithChildren<{isProtected: boolean}>): any {
    const location = useLocation();
    const {children, isProtected} = props;

    if (isProtected) {
        return !isAuth()
            ? (
                <Navigate to={paths.DEFAULT}
                          state={{from: location}}/>
            ) : children;
    }

    return isAuth()
        ? (
            <Navigate to={paths.SETS}
                      state={{from: location}}/>
        ) : children;
}