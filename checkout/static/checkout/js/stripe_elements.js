const stripePublicKey = JSON.parse(
  document.getElementById('id_stripe_public_key').textContent
);  
const clientSecret = JSON.parse(
  document.getElementById('id_client_secret').textContent
);  

// Initialize Stripe & Elements
const stripe = Stripe(stripePublicKey);
const elements = stripe.elements();

// Card style & mount
const style = {
  base: {
    color: '#000',
    fontFamily: '"Helvetica Neue", Helvetica, sans-serif',
    fontSmoothing: 'antialiased',
    fontSize: '16px',
    '::placeholder': { color: '#aab7c4' }
  },
  invalid: { color: '#dc3545', iconColor: '#dc3545' }
};
const card = elements.create('card', { style });
card.mount('#card-element');

// Real-time validation errors 
card.on('change', function(event) {
  const errorDiv = document.getElementById('card-errors');
  if (event.error) {
    errorDiv.innerHTML = `
      <span class="icon" role="alert"><i class="fas fa-times"></i></span>
      <span>${event.error.message}</span>
    `;
  } else {
    errorDiv.textContent = '';
  }
});

// Handle form submit
const form = document.getElementById('payment-form');
form.addEventListener('submit', function(ev) {
  ev.preventDefault();

  // disable while processing
  card.update({ disabled: true });
  document.getElementById('submit-button').disabled = true;  //

  stripe.confirmCardPayment(clientSecret, {
    payment_method: { card: card }
  }).then(function(result) {
    if (result.error) {
      // show error & re-enable
      document.getElementById('card-errors').innerHTML = `
        <span class="icon"><i class="fas fa-times"></i></span>
        <span>${result.error.message}</span>
      `;
      card.update({ disabled: false });
      document.getElementById('submit-button').disabled = false;  // 

    } else if (result.paymentIntent.status === 'succeeded') {
      // inject and submit
      document.getElementById('payment_intent_id').value =
        result.paymentIntent.id;

      form.submit();
    }
  });
});