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
    paperSelected: {
        height: "78%",
        margin: theme.spacing.unit,
        padding: theme.spacing.unit * 2,
        'background-color': "#ccc"
    },
  });

class RepoList extends Component {

    componentDidMount() {
        if (!this.props.repos.length) {
            this.props.fetchRepos();
        }
    }

    state = {
        text: "",
        updateNoteId: null,
    }

    convertLanguage(lang) {
        if (lang === 'C#') {
            return 'csharp';
        }
        if (lang === 'CSS') {
            return 'css3';
        }
        if (lang === 'Shell') {
            return 'linux';
        }

        return lang.toLowerCase();
    }

    selectRepo(repo) {
        this.props.addRepo(repo);
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
                                <Paper className={!note.selected ? classes.paper : classes.paperSelected} onClick={() => this.selectRepo(note)}>
                                    <Typography variant="title">{note.name}</Typography>
                                    <Typography>{note.description}</Typography>
                                    {note.language === null ? ('') : (
                                        <Typography className={'language-icon'} alignitems="flex-end">
                                            <i className={`devicon-${this.convertLanguage(note.language)}-plain`}></i>
                                            <span>{note.language}</span>
                                        </Typography>
                                    )}
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
        addRepo: (repo) => {
            dispatch(repos.addRepo(repo));
        },
    }
}

RepoList.propTypes = {
    classes: PropTypes.object.isRequired,
};


export default withStyles(styles)(connect(mapStateToProps, mapDispatchToProps)(RepoList));
