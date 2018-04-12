import React, { Component } from 'react';
import {connect} from 'react-redux';
import PropTypes from 'prop-types';
import { withStyles } from 'material-ui/styles';

import Grid from 'material-ui/Grid';
import GridList, { GridListTile } from 'material-ui/GridList';
import Paper from 'material-ui/Paper';
import Typography from 'material-ui/Typography';

import {repos} from "../actions";

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
  });

class RepoList extends Component {

    componentDidMount() {
        this.props.fetchRepos();
    }

    state = {
        text: "",
        updateNoteId: null,
    }

    render() {
        const { classes } = this.props

        return (
            <div className={classes.root}>
                <Grid container>
                    <Grid item xs zeroMinWidth>
                        <Typography variant="display1">Repos</Typography>
                    </Grid>
                </Grid>
                {!this.props.repos.length ? (
                    <div>Loading...</div>
                ) : (
                    <GridList cellHeight={220} cols={3}>
                        {this.props.repos.map((note, id) => (
                            <GridListTile cols={1} key={`note_${note.url}`}>
                                <Paper className={classes.paper}>
                                    <Typography variant="title">{note.name}</Typography>
                                    <Typography><a href={`${note.url}`} target="_blank">view</a></Typography>
                                    <Typography alignitems="flex-end">by: something here</Typography>
                                </Paper>
                            </GridListTile>
                        ))}
                    </GridList>
            ) }
            </div>
        )
    }
}


const mapStateToProps = state => {
    return {
        repos: state.repos,
    }
}

const mapDispatchToProps = dispatch => {
    return {
        fetchRepos: () => {
            dispatch(repos.fetchRepos());
        },
    }
}

RepoList.propTypes = {
    classes: PropTypes.object.isRequired,
};


export default withStyles(styles)(connect(mapStateToProps, mapDispatchToProps)(RepoList));
