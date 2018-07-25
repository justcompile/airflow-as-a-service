const initialState = null;


export default function payments(state=initialState, action) {
    switch (action.type) {

        case 'MAKE_PAYMENT':
            return { ...action.payment };

        case 'PAYMENT_FAILURE':
            return { ...action.error };
        default:
            return state;
    }
}
