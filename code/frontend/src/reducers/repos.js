const initialState = [];


export default function repos(state=initialState, action) {

    switch (action.type) {

        case 'FETCH_REPOS':
            return [...state, ...action.repos];

        default:
            return state;
    }
}
