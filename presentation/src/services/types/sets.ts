import {ISet} from "../../utils/types";
import {GET_SETS_LIST_ERROR, GET_SETS_LIST_REQUEST, GET_SETS_LIST_SUCCESS} from "../actions/sets";

export interface ISetsState {
    sets: Array<ISet> | [],
    setsListRequest: boolean,
    setsListError: boolean,
}

interface IGetSetsListRequest {
    type: typeof GET_SETS_LIST_REQUEST
}

interface IGetSetsListSuccess {
    type: typeof GET_SETS_LIST_SUCCESS,
    sets: Array<ISet> | []
}

interface IGetSetsListError {
    type: typeof GET_SETS_LIST_ERROR
}

export type TSetsActions = IGetSetsListRequest | IGetSetsListSuccess | IGetSetsListError;

