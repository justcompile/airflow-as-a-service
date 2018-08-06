const initialState = {};


export default function errors(state=initialState, action) {
    switch (action.type) {

        case 'HTTP/REQUEST/ERROR':
            return {message: action.error.message, stack: action.error.stack};

        case 'CLEAR_ERRORS':
            return {};

        default:
            return state;
    }
}
