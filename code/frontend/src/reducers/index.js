import { combineReducers } from 'redux';
import repos from "./repos";
import clusters from "./clusters";
import cluster from "./cluster";


const airflowAsAServiceApp = combineReducers({
    repos,
    clusters,
    cluster,
})

export default airflowAsAServiceApp;
