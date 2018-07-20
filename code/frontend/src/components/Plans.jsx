import React, { Component } from 'react';
import {connect} from 'react-redux';
import PropTypes from 'prop-types';
import { withStyles } from 'material-ui/styles';

import Grid from 'material-ui/Grid';
import GridList, { GridListTile } from 'material-ui/GridList';
import Paper from 'material-ui/Paper';
import Typography from 'material-ui/Typography';
import List from '@material-ui/core/List';
import ListItem from '@material-ui/core/ListItem';
import ListItemText from '@material-ui/core/ListItemText';
import Divider from '@material-ui/core/Divider';

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
    componentWillMount() {
        this.props.fetchPlans()
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
                                        <ListItem>
                                        <ListItemText primary="Inbox" />
                                        </ListItem>
                                        <Divider />
                                        <ListItem divider>
                                        <ListItemText primary="Drafts" />
                                        </ListItem>
                                        <ListItem>
                                        <ListItemText primary="Trash" />
                                        </ListItem>
                                        <Divider light />
                                        <ListItem>
                                        <ListItemText primary="Spam" />
                                        </ListItem>
                                    </List>
                                </Paper>
                            </GridListTile>
                        ))}
                    </GridList>
                )}
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
