function submitPayment() {
  const csrftoken = document.querySelector("[name=csrfmiddlewaretoken]").value;
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
  }).then(function (response) {
      
  });
}
