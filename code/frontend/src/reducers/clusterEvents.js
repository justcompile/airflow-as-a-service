const initialState = [];


export default function clusterEvents(state=initialState, action) {
    switch (action.type) {

        case 'FETCH_CLUSTER_EVENTS':
            return [...action.events];

        default:
            return state;
    }
}
