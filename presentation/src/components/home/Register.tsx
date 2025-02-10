import {ReactElement} from "react";
import styles from './Home.module.css';
import {homePageTabs} from "../../utils/constants";

export default function Register({setSelected}: {setSelected: Function}): ReactElement {
    return (
        <div className={styles.container} onClick={() => setSelected(homePageTabs.LOGIN)}>
            Login
        </div>
    )
}