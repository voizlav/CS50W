document.addEventListener("DOMContentLoaded", () => {
  // Use buttons to toggle between views
  document.querySelector("#inbox").onclick = () => load_mailbox("inbox");
  document.querySelector("#sent").onclick = () => load_mailbox("sent");
  document.querySelector("#archived").onclick = () => load_mailbox("archive");
  document.querySelector("#compose").onclick = () => compose_email();

  document.querySelector("#compose-form").onsubmit = (e) => {
    e.preventDefault();
    send_email();
  };

  // By default, load the inbox
  load_mailbox("inbox");
});

const compose_email = () => {
  // Show compose view and hide other views
  document.querySelector("#emails-view").style.display = "none";
  document.querySelector("#compose-view").style.display = "block";

  // Clear out composition fields
  document.querySelector("#compose-recipients").value = "";
  document.querySelector("#compose-subject").value = "";
  document.querySelector("#compose-body").value = "";
};

const load_mailbox = (mailbox) => {
  // Show the mailbox and hide other views
  document.querySelector("#emails-view").style.display = "block";
  document.querySelector("#compose-view").style.display = "none";

  // Show the mailbox name
  document.querySelector("#emails-view").innerHTML = `<h3>${
    mailbox.charAt(0).toUpperCase() + mailbox.slice(1)
  }</h3>`;
};

const send_email = () => {
  const composeRecipients = document.querySelector("#compose-recipients");
  const composeSubject = document.querySelector("#compose-subject");
  const composeBody = document.querySelector("#compose-body");

  const body = JSON.stringify({
    recipients: composeRecipients.value,
    subject: composeSubject.value,
    body: composeBody.value,
  });

  fetch("/emails", { method: "POST", body: body })
    .then((res) => res.json())
    .then((data) => display_message(...Object.entries(data)[0]));
};

const display_message = (message_type, message) => {
  const info = document.querySelector("#display-info");

  info.classList.add("alert");
  info.setAttribute("role", "alert");
  info.textContent = message;
  if (message_type === "message") {
    info.classList.add("alert-primary");
  }
  if (message_type === "error") {
    info.classList.add("alert-danger");
  }
};
