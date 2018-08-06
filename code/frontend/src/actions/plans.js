import {errorHandler} from "./helpers"
import ApiClient from '../api'

const client = new ApiClient()

export const fetchPlans = () => {
    return dispatch => {
        return client.list('plans')
            .then(plans => {
                return dispatch({
                    type: 'FETCH_PLANS',
                    plans
                })
            })
            .catch((error) => errorHandler(dispatch, error));
    }
}