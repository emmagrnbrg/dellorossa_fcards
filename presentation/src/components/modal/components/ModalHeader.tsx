import styles from "./ModalHeader.module.css";
import {ReactElement} from "react";

/**
 * Заголовок модального окна
 */
export default function ModalHeader(props: {title?: string, onClick: Function}): ReactElement {
    const {title, onClick} = props;

    return (
        <section className={styles.modalHeader}
                 onClick={e => onClick(e)}>
            <p>
                {title}
            </p>
        </section>
    )
}