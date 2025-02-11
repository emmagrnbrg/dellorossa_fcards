import {ReactElement} from "react";
import styles from './Home.module.css';
import {homePageTabs} from "../../utils/constants";

export default function Login({setSelected}: {setSelected: Function}): ReactElement {
    return (
        <section className={styles.mainBody}>
            <section className={styles.container}>
                <p>
                    Добро пожаловать, это форма авторизации! Для регистрации нажмите кнопку:
                </p>
                <button className={styles.button} onClick={() => setSelected(homePageTabs.REGISTER)}>Example</button>
            </section>
        </section>
    )
}