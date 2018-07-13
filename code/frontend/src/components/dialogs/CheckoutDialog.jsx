import React from 'react';
import {Elements, StripeProvider} from 'react-stripe-elements';

import SubscriptionForm from './SubscriptionForm';

class CheckoutDialog extends React.Component {
  render() {
    return (
        <StripeProvider apiKey="pk_test_12345">
            <Elements>
                <SubscriptionForm />
            </Elements>
        </StripeProvider>
    );
  }
}

export default CheckoutDialog;