const initialState = [];


export default function github(state=initialState, action) {
    switch (action.type) {
        case 'FETCH_REMOTE_REPOS':
            return [...state, ...action.repos];

        case 'ADD_REPO':
            const clone = [...state];
            clone[clone.findIndex(element => element.url === action.repo.url)].selected = action.repo.selected;
            return clone;

        default:
            return state;
    }
}
