const initialState = null;


export default function plans(state=initialState, action) {
    switch (action.type) {

        case 'FETCH_PLANS':
            return [ ...action.plans ];

        case 'MAKE_PAYMENT':
            const tempState = [...state];
            const idx = tempState.findIndex(item => action.payment.id === item.id);
            tempState[idx] = action.payment;
            return tempState;

        default:
            return state;
    }
}
