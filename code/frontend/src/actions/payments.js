import {errorHandler} from "./helpers"
import ApiClient from '../api'

const client = new ApiClient()

export const makePayment = (token, plan) => {
    return dispatch => {
        return client.raw('/api/subscribe', "POST", {token, plan})
            .then(payment => {
                return dispatch({
                    type: 'MAKE_PAYMENT',
                    payment
                })
            })
            .catch((error) => errorHandler(dispatch, error));
    }
}