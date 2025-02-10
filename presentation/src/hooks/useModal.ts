import { useState, useCallback } from "react";

/**
 * Хук для управления модальным окном
 */
export const useModal = (): {isModalOpen: boolean, openModal: Function, closeModal: Function} => {
    const [isModalOpen, setIsModalOpen] = useState(false);

    const openModal = useCallback((): void => {
        setIsModalOpen(true);
    }, []);

    const closeModal = useCallback((): void => {
        setIsModalOpen(false);
    }, []);

    return {
        isModalOpen,
        openModal,
        closeModal,
    };
};