import { updateStateFromSocket } from './helpers';

const initialState = [];


export default function builds(state=initialState, action) {
    switch (action.type) {

        case 'FETCH_BUILDS':
            return [...action.builds];

        case 'WEBSOCKET/EVENT/MESSAGE':
            return updateStateFromSocket('builds', state, action);
        
        default:
            return state;
    }
}
