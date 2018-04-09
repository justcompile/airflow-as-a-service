const initialState = [];


export default function clusters(state=initialState, action) {

    switch (action.type) {

        case 'FETCH_CLUSTERS':
            return [...action.clusters];
        
        case 'ADD_CLUSTER':
            return [...state, action.cluster];

        default:
            return state;
    }
}
