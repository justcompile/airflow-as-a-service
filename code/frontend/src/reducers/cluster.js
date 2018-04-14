const initialState = null;


export default function clusters(state=initialState, action) {
    switch (action.type) {

        case 'FETCH_CLUSTER':
            return { ...action.cluster };

        default:
            return state;
    }
}
