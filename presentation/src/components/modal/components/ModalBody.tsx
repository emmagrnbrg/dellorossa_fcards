import styles from "./ModalBody.module.css";
import {PropsWithChildren, ReactElement} from "react";

/**
 * Тело модального окна
 */
export default function ModalBody(props: PropsWithChildren<{}>): ReactElement {
    return (
        <section className={styles.modalBody}>
            {props.children}
        </section>
    )
}