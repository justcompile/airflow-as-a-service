import { combineReducers } from 'redux';
import repos from "./repos";
import github from "./github";
import clusters from "./clusters";
import cluster from "./cluster";
import clusterEvents from "./clusterEvents";
import dbTypes from "./dbTypes";


const airflowAsAServiceApp = combineReducers({
    clusters,
    cluster,
    clusterEvents,
    dbTypes,
    github,
    repos,
})

export default airflowAsAServiceApp;
