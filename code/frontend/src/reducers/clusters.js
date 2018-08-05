import { updateStateFromSocket } from './helpers';
const initialState = [];


export default function clusters(state=initialState, action) {
    switch (action.type) {

        case 'FETCH_CLUSTERS':
            return [...action.clusters];
        
        case 'ADD_CLUSTER':
            return [...state, action.cluster];

        case 'DELETE_CLUSTER':
            return [...state.filter(item => action.clusterId !== item.id)];

        case 'WEBSOCKET/EVENT/MESSAGE':
            return updateStateFromSocket('clusters', state, action);

        default:
            return state;
    }
}
