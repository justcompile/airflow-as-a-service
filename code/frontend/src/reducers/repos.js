const initialState = [];


export default function repos(state=initialState, action) {

    switch (action.type) {

        case 'FETCH_REPOS':
            return [...state, ...action.repos];

        case 'ADD_REPO':
            const clone = [...state];
            clone[clone.findIndex(element => element.url === action.repo.url)].selected = action.repo.selected;
            return clone;

        default:
            return state;
    }
}
