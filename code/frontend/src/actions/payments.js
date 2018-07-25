import ApiClient from '../api'

const client = new ApiClient()

export const makePayment = (token, plan) => {
    return dispatch => {
        return client.raw('/pay/subscribe', "POST", {token, plan})
            .then(payment => {
                return dispatch({
                    type: 'MAKE_PAYMENT',
                    payment
                })
            }).catch(e => {
                return dispatch({
                    type: 'PAYMENT_FAILURE',
                    error: e
                })
            })
    }
}