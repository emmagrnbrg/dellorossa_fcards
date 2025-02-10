import styles from "./ModalOverlay.module.css";
import {ReactElement} from "react";

/**
 * Оверлей модального окна
 */
export default function ModalOverlay(props: {onClick?: Function}): ReactElement {
    const {onClick} = props;

    return (
        <section className={styles.modalOverlay} onClick={e => onClick && onClick(e)}/>
    )
}