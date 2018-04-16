import { combineReducers } from 'redux';
import repos from "./repos";
import clusters from "./clusters";
import cluster from "./cluster";
import clusterEvents from "./clusterEvents";


const airflowAsAServiceApp = combineReducers({
    repos,
    clusters,
    cluster,
    clusterEvents,
})

export default airflowAsAServiceApp;
