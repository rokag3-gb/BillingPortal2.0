function submitPayment() {
  $("#paymentModal").modal('show');
  const paymentProgress = document.getElementById("payment-progress");
  const paymentSuccess = document.getElementById("payment-success");
  const paymentError = document.getElementById("payment-error");
  const paymentErrorContainer = document.getElementById(
    "payment-error-container"
  );
  const csrftoken = document.querySelector("[name=csrfmiddlewaretoken]").value;
  paymentErrorContainer.hidden = true;
  fetch("charge/", {
    method: "POST",
    credentials: "same-origin",
    headers: {
      "Content-Type": "application/x-www-form-urlencoded",
      "X-CSRFToken": csrftoken,
    },
    body: JSON.stringify({
      card_owner: document.getElementById("card_owner").value,
      owner_proof: document.getElementById("owner_proof").value,
      owner_email: document.getElementById("owner_email").value,
      phone_number: document.getElementById("phone_number").value,
      card_number: document.getElementById("card_number").value,
      valid_until: document.getElementById("valid_until").value,
      card_password: document.getElementById("card_password").value,
    }),
  })
    .then(function (response) {
      paymentProgress.hidden = true;
      if (response.ok) {
        paymentSuccess.hidden = false;
      } else if (response.status >= 400 && response.status < 500) {
        response.json().then(function(json){
          paymentErrorContainer.hidden = false;
          paymentError.innerText = `결제 중 오류가 발생했습니다. 입력하신 정보를 다시 확인하세요: ${json['응답메시지']}`;
        })
      } else if (response.status >= 500 && response.status < 600) {
        paymentErrorContainer.hidden = false;
        paymentError.innerText = "결제 처리 중 서버 내부 오류가 발생했습니다.";
      }
    })
    .catch(function (error) {
      console.log(error);
      paymentErrorContainer.hidden = false;
      paymentError.innerText = "서버와 통신 중 오류가 발생했습니다.";
    });
}

function resetPaymentDialog() {
  // document.getElementById("card_owner").value = "";
  // document.getElementById("owner_proof").value = "";
  // document.getElementById("owner_email").value = "";
  // document.getElementById("phone_number").value = "";
  // document.getElementById("card_number").value = "";
  // document.getElementById("valid_until").value = "";
  // document.getElementById("card_password").value = "";
  const paymentForm = document.getElementById("payment-form");
  const paymentProgress = document.getElementById("payment-progress");
  const paymentSuccess = document.getElementById("payment-success");
  const paymentError = document.getElementById("payment-error");
  const paymentErrorContainer = document.getElementById(
    "payment-error-container"
  );
  paymentProgress.hidden = false;
  paymentSuccess.hidden = true;
  paymentError.innerText = "";
  paymentErrorContainer.hidden = true;
}
