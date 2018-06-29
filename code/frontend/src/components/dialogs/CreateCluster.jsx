import React from 'react';
import PropTypes from 'prop-types';
import Button from 'material-ui/Button';
import { withStyles } from 'material-ui/styles';
import Dialog, { DialogActions, DialogContent, DialogTitle } from 'material-ui/Dialog';
import Input, { InputLabel } from 'material-ui/Input';
import { MenuItem } from 'material-ui/Menu';
import { FormControl } from 'material-ui/Form';
import Select from 'material-ui/Select';

import {connect} from 'react-redux';
import {clusters, repos} from "../../actions";

const styles = theme => ({
  container: {
    display: 'flex',
    flexWrap: 'wrap',
  },
  formControl: {
    margin: theme.spacing.unit,
    minWidth: 240,
  },
});

class CreateClusterDialog extends React.Component {
  state = {
    open: false,
    submitted: false,
    dbType: '',
    repository: ''
  };

  componentDidMount() {
    this.props.fetchDBTypes();
    this.props.fetchRepos();
  }

  handleChange = name => event => {
    this.setState({ [name]: event.target.value });
  };

  handleSubmit = () => {
    this.setState({'submitted': true})
    if (this.state.dbType !== '' && this.state.repository !== '') {
      this.props.onSubmit({
        dbType: this.state.dbType,
        repository: this.state.repository
      });
    }
  };

  render() {
    const { classes, open } = this.props;

    if (this.props.dbTypes == null || this.props.repos == null) {
        return null;
    }

    return (
      <div>
        <Dialog
          disableBackdropClick
          disableEscapeKeyDown
          open={open}
          onClose={this.handleClose}
        >
          <DialogTitle>Create Cluster</DialogTitle>
          <DialogContent>
            <form className={classes.container}>
            {this.state.error ? (
              <p>{this.state.error}</p>
            ) : ('')}
              <FormControl className={classes.formControl}>
                <InputLabel htmlFor="db-simple">Airflow MetaDB Type</InputLabel>
                <Select
                  error={this.state.submitted && this.state.dbType === ''}
                  value={this.state.dbType}
                  onChange={this.handleChange('dbType')}
                  input={<Input id="db-simple" />}
                >
                  {this.props.dbTypes.map((dbType, id) => (
                    <MenuItem key={id} value={dbType.id}>{dbType.varient} {dbType.version}</MenuItem>
                  ))}
                </Select>
              </FormControl>
              <FormControl className={classes.formControl}>
                <InputLabel htmlFor="repo-simple">Repository</InputLabel>
                <Select
                  error={this.state.submitted && this.state.repository === ''}
                  value={this.state.repository}
                  onChange={this.handleChange('repository')}
                  input={<Input id="repo-simple" />}
                >
                  {this.props.repos.map((repo, id) => (
                    <MenuItem key={id} value={repo.id}>{repo.name}</MenuItem>
                  ))}
                </Select>
              </FormControl>
            </form>
          </DialogContent>
          <DialogActions>
            <Button onClick={this.props.onCancel} color="primary">
              Cancel
            </Button>
            <Button onClick={this.handleSubmit} color="primary">
              Ok
            </Button>
          </DialogActions>
        </Dialog>
      </div>
    );
  }
}

const mapStateToProps = state => {
    return {
        dbTypes: state.dbTypes,
        repos: state.repos,
    }
}

const mapDispatchToProps = dispatch => {
    return {
        fetchDBTypes: () => {
            dispatch(clusters.fetchDBTypes());
        },
        fetchRepos: () => {
          dispatch(repos.fetchUserRepos());
        }
    }
}

CreateClusterDialog.propTypes = {
  classes: PropTypes.object.isRequired,
  open: PropTypes.bool.isRequired,
  onCancel: PropTypes.func.isRequired,
  onSubmit: PropTypes.func.isRequired,
};

export default withStyles(styles)(connect(mapStateToProps, mapDispatchToProps)(CreateClusterDialog));