import React from 'react';
import {connect} from 'react-redux';
import PropTypes from 'prop-types';
import classNames from 'classnames';
import {injectStripe} from 'react-stripe-elements';
import { withStyles } from '@material-ui/core/styles';
import CircularProgress from '@material-ui/core/CircularProgress';
import green from '@material-ui/core/colors/green';
import Button from '@material-ui/core/Button';
import CardSection from './CardSection';

import {payments} from "../actions";


const styles = theme => ({
  formContainer: {
    width: 400,
  },
  wrapper: {
    margin: theme.spacing.unit,
    position: 'relative',
    display: 'inline',
  },
  progress: {
    margin: theme.spacing.unit * 2,
  },
  buttonSuccess: {
    backgroundColor: green[500],
    '&:hover': {
      backgroundColor: green[700],
    },
  },
  buttonProgress: {
    color: green[500],
    position: 'absolute',
    top: '50%',
    left: '50%',
    marginTop: -12,
    marginLeft: -12,
  },
});

class SubscriptionForm extends React.Component {
  constructor() {
    super();
    this.state = {loading: false, success: false};
  }

  componentWillUpdate(nextProps, nextState) {
    if (nextProps.payment !== undefined && nextProps.payment !== null && !this.state.success) {
      this.state.loading = false;
      this.state.success = true;
      const self = this;
      setTimeout(() => {self.props.onSuccess()}, 2000);
    }
  }

  handleSubmit = (ev) => {
    // We don't want to let default form submission happen here, which would refresh the page.
    ev.preventDefault();
    
    if (!this.state.success && !this.state.loading) {
      this.setState({loading: true});

      // Within the context of `Elements`, this call to createToken knows which Element to
      // tokenize, since there's only one in this group.
      this.props.stripe.createToken({name: this.props.user.email}).then(({token}) => {
        if (token === undefined) {
          this.setState({loading: false});
        } else {
          this.props.makePayment(token, this.props.plan)
        }
        console.log('Received Stripe token:', token);
      });
    }
  };

  render() {
    const { classes } = this.props;
    const { loading, success } = this.state;
    const buttonClassname = classNames({
      [classes.buttonSuccess]: success,
    }); 

    return (
      <form className={classes.formContainer} onSubmit={this.handleSubmit}>
        <CardSection />
        <div className={classes.wrapper}>
          <Button
            color="primary"
            variant="contained"
            onClick={this.handleSubmit}
            disabled={loading}
            className={buttonClassname}
          >{this.state.success ? 'Subscribed!' : 'Confirm order'}</Button>
          {loading && <CircularProgress size={24} className={classes.buttonProgress} />}
        </div>
      </form>
    );
  }
}

const mapStateToProps = state => {
  return {
      payment: state.payments,
  }
}

const mapDispatchToProps = dispatch => {
  return {
      makePayment: (token, plan) => {
          dispatch(payments.makePayment(token, plan));
      },
  }
}

SubscriptionForm.propTypes = {
  user: PropTypes.object.isRequired,
  plan: PropTypes.object.isRequired,
  onSuccess: PropTypes.func.isRequired,
};

export default withStyles(styles)(connect(mapStateToProps, mapDispatchToProps)(injectStripe(SubscriptionForm)));