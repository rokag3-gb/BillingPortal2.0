function submitPayment() {
  const paymentForm = document.getElementById("payment-form");
  const paymentProgress = document.getElementById("payment-progress");
  const paymentSuccess = document.getElementById("payment-success");
  const paymentError = document.getElementById("payment-error");
  const paymentErrorContainer = document.getElementById(
    "payment-error-container"
  );
  const csrftoken = document.querySelector("[name=csrfmiddlewaretoken]").value;

  paymentErrorContainer.hidden = true;
  paymentForm.hidden = true;
  paymentProgress.hidden = false;
  fetch("", {
    method: "POST",
    credentials: "same-origin",
    headers: {
      "Content-Type": "application/x-www-form-urlencoded",
      "X-CSRFToken": csrftoken,
    },
    body: JSON.stringify({
      card_owner: document.getElementById("card_owner").value,
      owner_birthday: document.getElementById("owner_birthday").value,
      owner_email: document.getElementById("owner_email").value,
      phone_number: document.getElementById("phone_number").value,
      card_number: document.getElementById("card_number").value,
      valid_until: document.getElementById("valid_until").value,
      card_password: document.getElementById("card_password").value,
    }),
  })
    .then(function (response) {
      if (response.ok) {
        paymentProgress.hidden = true;
        paymentSuccess.hidden = false;
      }
    })
    .catch(function (error) {
      paymentForm.hidden = false;
      paymentErrorContainer.hidden = false;
      paymentError.innerText = "서버와 통신 중 오류가 발생했습니다.";
    });
}

function resetPaymentDialog(){
  document.getElementById("card_owner").value = "";
  document.getElementById("owner_birthday").value = "";
  document.getElementById("owner_email").value = "";
  document.getElementById("phone_number").value = "";
  document.getElementById("card_number").value = "";
  document.getElementById("valid_until").value = "";
  document.getElementById("card_password").value = "";
  const paymentForm = document.getElementById("payment-form");
  const paymentProgress = document.getElementById("payment-progress");
  const paymentSuccess = document.getElementById("payment-success");
  const paymentError = document.getElementById("payment-error");
  const paymentErrorContainer = document.getElementById(
    "payment-error-container"
  );
  paymentForm.hidden = false;
  paymentProgress.hidden = true;
  paymentSuccess.hidden = true;
  paymentError.hidden = true;
  paymentErrorContainer.hidden = true;
}