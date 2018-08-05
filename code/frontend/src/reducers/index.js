import { combineReducers } from 'redux';
import repos from "./repos";
import github from "./github";
import clusters from "./clusters";
import cluster from "./cluster";
import clusterEvents from "./clusterEvents";
import dbTypes from "./dbTypes";
import payments from "./payments";
import plans from "./plans";
import builds from "./builds";
import errors from "./errors";

const airflowAsAServiceApp = combineReducers({
    clusters,
    cluster,
    clusterEvents,
    dbTypes,
    github,
    repos,
    payments,
    plans,
    builds,
    errors,
})

export default airflowAsAServiceApp;
