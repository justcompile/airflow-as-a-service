const initialState = [];


export default function builds(state=initialState, action) {
    switch (action.type) {

        case 'FETCH_BUILDS':
            return [...action.builds];
        
        default:
            return state;
    }
}
