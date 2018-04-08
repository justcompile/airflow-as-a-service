import { combineReducers } from 'redux';
import repos from "./repos";
import clusters from "./clusters";


const airflowAsAServiceApp = combineReducers({
    repos,
    clusters,
})

export default airflowAsAServiceApp;
