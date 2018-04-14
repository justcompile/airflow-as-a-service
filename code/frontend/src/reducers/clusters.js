const initialState = [];


export default function clusters(state=initialState, action) {
    switch (action.type) {

        case 'FETCH_CLUSTERS':
            return [...action.clusters];
        
        case 'ADD_CLUSTER':
            return [...state, action.cluster];

        case 'DELETE_CLUSTER':
            state.splice(state.indexOf(action.cluster), 1);

            return [...state];

        default:
            return state;
    }
}
