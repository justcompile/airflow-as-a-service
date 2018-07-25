import React, { Component } from 'react';
import {connect} from 'react-redux';
import PropTypes from 'prop-types';
import { withStyles } from '@material-ui/core/styles';

import Button from '@material-ui/core/Button';
import Grid from '@material-ui/core/Grid';
import GridList from '@material-ui/core/GridList';
import GridListTile from '@material-ui/core/GridListTile';
import Paper from '@material-ui/core/Paper';
import Typography from '@material-ui/core/Typography';
import List from '@material-ui/core/List';
import ListItem from '@material-ui/core/ListItem';
import ListItemText from '@material-ui/core/ListItemText';

import CheckoutDialog from './dialogs/CheckoutDialog';


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
    defaultState = { open: false, plan: null }

    constructor(props) {
        super(props)
        this.state = this.defaultState
    }

    componentWillMount() {
        this.props.fetchPlans()
    }

    openPaymentModal(plan) {
        this.setState({open: true, plan});
    }

    render() {
        // const { classes } = this.props

        return (
            <div>
                <Grid container>
                    <Grid item xs zeroMinWidth>
                        <Typography variant="display1">Plans</Typography>
                    </Grid>
                </Grid>
                {! this.props.plans || !this.props.plans.length ? (
                    <div>Loading...</div>
                ) : (
                    <GridList cellHeight={240} cols={this.props.plans.length}>
                        {this.props.plans.map((plan, id) => (
                            <GridListTile cols={1} key={plan.id}>
                                <Paper>
                                    <Typography variant="title">{plan.name}</Typography>
                                    <List>
                                        {plan.features.map((feature, featureId) => (
                                            <ListItem key={`{feature.key}-{feature.value}`} divider>
                                                <ListItemText primary={feature.name + ": " + feature.value}/>
                                            </ListItem>
                                        ))}
                                        <ListItem>
                                            {plan.subscribed ? (
                                                <Button variant="raised" color="primary" disabled>Subscribed</Button>
                                            ) : (
                                                <Button variant="raised" color="primary" onClick={() => this.openPaymentModal(plan)}>Buy</Button>
                                            )}
                                        </ListItem>
                                    </List>
                                </Paper>
                            </GridListTile>
                        ))}
                    </GridList>
                )}
                <CheckoutDialog open={this.state.open} plan={this.state.plan} />
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
