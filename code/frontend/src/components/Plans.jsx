import React, { Component } from 'react';
import {connect} from 'react-redux';
import PropTypes from 'prop-types';
import { withStyles } from 'material-ui/styles';

import {plans} from "../actions";

const styles = theme => ({
    root: {
        display: 'flex',
        flexWrap: 'wrap',
        justifyContent: 'space-around',
        overflow: 'hidden',
    },
    paper: {
        height: "78%",
        margin: theme.spacing.unit,
        padding: theme.spacing.unit * 2,
    },
    paperSelected: {
        height: "78%",
        margin: theme.spacing.unit,
        padding: theme.spacing.unit * 2,
        'background-color': "#ccc"
    },
  });

class Plans extends Component {
    render() {
        const { classes } = this.props

        return (
            <div>
                Plans here
            </div>   
        )
    }
}


const mapStateToProps = state => {
    return {
        plans: state.plans,
    }
}

const mapDispatchToProps = dispatch => {
    return {
        fetchPlans: () => {
            dispatch(plans.fetchPlans());
        },
    }
}

Plans.propTypes = {
    classes: PropTypes.object.isRequired,
};


export default withStyles(styles)(connect(mapStateToProps, mapDispatchToProps)(Plans));
