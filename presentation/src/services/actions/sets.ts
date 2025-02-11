import {Dispatch} from "react";
import {TSetsActions} from "../types/sets";

export const GET_SETS_LIST_REQUEST: "GET_SETS_LIST_REQUEST" = "GET_SETS_LIST_REQUEST";
export const GET_SETS_LIST_SUCCESS: "GET_SETS_LIST_SUCCESS" = "GET_SETS_LIST_SUCCESS";
export const GET_SETS_LIST_ERROR: "GET_SETS_LIST_ERROR" = "GET_SETS_LIST_ERROR";

export function getSetsListAction() {
    return function(dispatch: Dispatch<TSetsActions>) {
        dispatch({
            type: GET_SETS_LIST_REQUEST
        });
        getIngredientList()
            .then(response => {
                if (response && response.success) {
                    dispatch({
                        type: GET_AVAILABLE_INGREDIENTS_SUCCESS,
                        availableIngredients: response.data
                    });
                } else {
                    dispatch({
                        type: GET_AVAILABLE_INGREDIENTS_ERROR
                    });
                }
            })
            .catch(() => {
                dispatch({
                    type: GET_AVAILABLE_INGREDIENTS_ERROR
                })
            });
    }
}