import React from 'react';

import PropTypes from 'prop-types';
import { withStyles } from '@material-ui/core/styles';
import Dialog from '@material-ui/core/Dialog';
import DialogContent from '@material-ui/core/DialogContent';
import DialogTitle from '@material-ui/core/DialogTitle';

import {Elements, StripeProvider} from 'react-stripe-elements';

import SubscriptionForm from '../SubscriptionForm';

const styles = theme => ({
    container: {
      display: 'flex',
      flexWrap: 'wrap',
      minWidth: 400,
    },
  });

class CheckoutDialog extends React.Component {

    constructor() {
        super();
        this.state = {stripe: null, user: null};
    }
    componentDidMount() {
        const jsElement = document.querySelector('#stripe-js');
        const data = JSON.parse(document.getElementById('rjs-data').innerText);
        this.setState({user: data.user});
        if (window.Stripe) {
          this.setState({stripe: window.Stripe(data.stripeKey)});
        } else {
            jsElement.addEventListener('load', () => {
            // Create Stripe instance once Stripe.js loads
            this.setState({stripe: window.Stripe(data.stripeKey)});
          });
        }
      }

  render() {
    const { classes, open } = this.props;

    return (
        <StripeProvider stripe={this.state.stripe}>
            <Dialog
            disableBackdropClick
            disableEscapeKeyDown
            open={open}>
                <DialogTitle>Subscribe</DialogTitle>
                <DialogContent>
                    <Elements>
                        <SubscriptionForm user={this.state.user} plan={this.props.plan} onSuccess={this.props.onSuccess}/>
                    </Elements>
                </DialogContent>
            </Dialog>
        </StripeProvider>
    );
  }
}

function allowNull(wrappedPropTypes) {
    return (props, propName, ...rest) => {
        if (props[propName] === null) return null;
        return wrappedPropTypes(props, propName, ...rest);
    }
}

CheckoutDialog.propTypes = {
    classes: PropTypes.object.isRequired,
    open: PropTypes.bool.isRequired,
    plan: allowNull(PropTypes.object.isRequired),
    onSuccess: PropTypes.func.isRequired,
};
  

export default withStyles(styles)(CheckoutDialog);