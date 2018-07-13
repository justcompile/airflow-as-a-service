const initialState = null;


export default function plans(state=initialState, action) {
    switch (action.type) {

        case 'FETCH_PLANS':
            return [ ...action.plans ];

        default:
            return state;
    }
}
