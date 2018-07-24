import React from 'react';
import PropTypes from 'prop-types';
import classNames from 'classnames';
import {injectStripe} from 'react-stripe-elements';
import { withStyles } from '@material-ui/core/styles';
import CircularProgress from '@material-ui/core/CircularProgress';
import green from '@material-ui/core/colors/green';
import Button from '@material-ui/core/Button';
import CardSection from './CardSection';



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

  handleSubmit = (ev) => {
    // We don't want to let default form submission happen here, which would refresh the page.
    ev.preventDefault();
    
    if (!this.state.loading) {
      this.setState({loading: true});

      // Within the context of `Elements`, this call to createToken knows which Element to
      // tokenize, since there's only one in this group.
      this.props.stripe.createToken({name: this.props.user.email}).then(({token}) => {
        if (token === undefined) {
          this.setState({loading: false});
        } else {
          this.setState({loading: false, success: true});
        }
        console.log('Received Stripe token:', token);
      });
    }

    // However, this line of code will do the same thing:
    //
    // this.props.stripe.createToken({type: 'card', name: 'Jenny Rosen'});

    // You can also use createSource to create Sources. See our Sources
    // documentation for more: https://stripe.com/docs/stripe-js/reference#stripe-create-source
    //
    // this.props.stripe.createSource({type: 'card', name: 'Jenny Rosen'});
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
          >Confirm order</Button>
          {loading && <CircularProgress size={24} className={classes.buttonProgress} />}
        </div>
      </form>
    );
  }
}

SubscriptionForm.propTypes = {
  user: PropTypes.object.isRequired,
};

export default withStyles(styles)(injectStripe(SubscriptionForm));