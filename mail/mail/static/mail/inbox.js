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
  remove_message();
  remove_display_email();

  // Show compose view and hide other views
  document.querySelector("#emails-view").style.display = "none";
  document.querySelector("#compose-view").style.display = "block";

  // Clear out composition fields
  document.querySelector("#compose-recipients").value = "";
  document.querySelector("#compose-subject").value = "";
  document.querySelector("#compose-body").value = "";
};

const reply_email = (email_id) => {
  remove_message();
  remove_display_email();

  document.querySelector("#emails-view").style.display = "none";
  document.querySelector("#compose-view").style.display = "block";

  fetch(`/emails/${email_id}`)
    .then((res) => res.json())
    .then((data) => {
      document.querySelector("#compose-recipients").value = data.sender;
      document.querySelector("#compose-subject").value =
        data.subject.slice(0, 3) === "Re:"
          ? data.subject
          : `Re: ${data.subject}`;
      document.querySelector(
        "#compose-body",
      ).value = `"${data.timestamp} ${data.sender} wrote:\n${data.body}"`;
    });
};

const load_mailbox = (mailbox) => {
  remove_message();
  remove_display_email();

  // Show the mailbox and hide other views
  document.querySelector("#emails-view").style.display = "block";
  document.querySelector("#compose-view").style.display = "none";

  // Show the mailbox name
  document.querySelector("#emails-view").innerHTML = `<h3>${
    mailbox.charAt(0).toUpperCase() + mailbox.slice(1)
  }</h3>`;

  load_emails(mailbox);
};

const load_emails = (mailbox) => {
  const emails_view = document.querySelector("#emails-view");
  const list_emails = document.createElement("ul");
  list_emails.className = "list-group";
  emails_view.appendChild(list_emails);

  fetch(`/emails/${mailbox}`)
    .then((res) => res.json())
    .then((data) =>
      data.forEach((email) => {
        const list_email_item = document.createElement("li");
        const email_sender = document.createElement("div");
        const email_subject = document.createElement("div");
        const email_timestamp = document.createElement("span");
        list_email_item.classList.add(
          "list-group-item",
          "d-flex",
          "justify-content-between",
          "align-items-start",
          email.read ? "bg-secondary" : "bg-white",
          email.read ? "bg-opacity-10" : "bg-opacity",
        );
        email_timestamp.classList.add(
          "badge",
          "rounded-pill",
          "bg-opacity-75",
          email.read ? "bg-secondary" : "bg-primary",
        );
        email_sender.classList.add("ms-2", "me-auto");
        email_subject.classList.add(
          "fw-bold",
          email.read ? "text-muted" : "text",
        );

        if (mailbox === "archive" && email.archived) {
          email_sender.innerText = email.sender;
          email_subject.innerText = email.subject;
          email_timestamp.innerText = email.timestamp;
        } else {
          email_sender.innerText = email.sender;
          email_subject.innerText = email.subject;
          email_timestamp.innerText = email.timestamp;
        }
        list_email_item.appendChild(email_sender);
        email_sender.appendChild(email_subject);
        list_email_item.appendChild(email_timestamp);
        list_emails.appendChild(list_email_item);

        list_email_item.onclick = () => display_email(mailbox, email.id);
      }),
    );
};

const display_email = (mailbox, email_id) => {
  remove_display_email();
  document.querySelector("#emails-view").style.display = "none";
  document.querySelector("#compose-view").style.display = "none";

  fetch(`/emails/${email_id}`)
    .then((res) => res.json())
    .then((data) => {
      const mail = document.querySelector("#email-view");
      const main_card = document.createElement("div");
      const card_header = document.createElement("div");
      const from_to = document.createElement("p");
      const card_body = document.createElement("div");
      const card_title = document.createElement("h5");
      const card_footer = document.createElement("div");
      const timestamp = document.createElement("p");
      const reply = document.createElement("a");
      const archive = document.createElement("a");

      main_card.classList.add("card");
      card_body.classList.add("card-body");
      card_header.classList.add("card-header");
      from_to.classList.add("card-text", "text-muted");
      card_title.classList.add("card-title");

      card_footer.classList.add("card-footer", "bg-white");
      timestamp.classList.add("card-text", "text-muted");
      reply.classList.add("btn", "btn-primary", "btn-sm", "mt-3");

      from_to.textContent = `From ${data.sender} `;
      from_to.textContent += `to ${data.recipients.join(", ")}`;
      card_title.textContent = data.subject;
      timestamp.textContent = data.timestamp;
      reply.textContent = "Reply";

      card_header.appendChild(from_to);
      main_card.appendChild(card_header);
      card_body.appendChild(card_title);
      data.body.split("\n").forEach((line) => {
        const card_text = document.createElement("p");
        card_text.classList.add("card-text");
        card_text.textContent = line;
        card_body.appendChild(card_text);
      });
      main_card.appendChild(card_body);
      card_footer.appendChild(timestamp);
      main_card.appendChild(card_footer);
      mail.appendChild(main_card);
      mail.appendChild(reply);
      reply.onclick = () => reply_email(email_id);
      if (mailbox !== "sent") {
        archive.classList.add("btn", "btn-primary", "btn-sm", "mt-3", "ms-3");
        archive.textContent = data.archived ? "Unarchive" : "Archive";
        mail.appendChild(archive);
        archive.onclick = () => archive_mail(data.archived, email_id);
      }

      mark_email_as_read(email_id);
    });
};

const archive_mail = (is_archive, email_id) => {
  fetch(`/emails/${email_id}`, {
    method: "PUT",
    body: JSON.stringify({ archived: is_archive ? false : true }),
  }).then(location.reload());
};

const remove_display_email = () => {
  const email = document.querySelector("#email-view");
  email.innerHTML = "";
};

const mark_email_as_read = (email_id) => {
  fetch(`/emails/${email_id}`, {
    method: "PUT",
    body: JSON.stringify({ read: true }),
  });
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

const remove_message = () => {
  const info = document.querySelector("#display-info");

  info.textContent = "";
  info.removeAttribute("class");
  info.removeAttribute("role");
};
