import {ReactElement, useState} from "react";
import Login from "../components/home/Login";
import {homePageTabs} from "../utils/constants";
import Register from "../components/home/Register";

export default function HomePage(): ReactElement {
    const [selected, setSelected] = useState(homePageTabs.LOGIN);

    return (
        <>
            {
                selected === homePageTabs.LOGIN && <Login setSelected={setSelected}/>
            }
            {
                selected === homePageTabs.REGISTER && <Register setSelected={setSelected}/>
            }
        </>
    )
}