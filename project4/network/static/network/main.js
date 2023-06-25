const init = () => {
  document.addEventListener("DOMContentLoaded", () => {
    likes();
    createNewPost();
    editPost();
  });
};

const createNewPost = () => {
  const newPost = document.querySelector("#newPost");
  const newPostButton = document.querySelector("#newPostButton");
  if (newPostButton)
    newPostButton.onclick = () => {
      fetch("/newpost", {
        method: "POST",
        body: JSON.stringify({ content: newPost.value }),
      })
        .then((res) => res.json())
        .then((data) => {
          if (data.message) {
            window.location.href = "/";
          }
        });
    };
};

const editPost = () => {
  const allButtons = document.querySelectorAll(".edit-button");
  allButtons.forEach((btn) => {
    btn.onclick = (e) => {
      const postDiv = e.target.parentNode.parentNode.parentNode;
      const postPara = postDiv.querySelector("p");
      const textArea = document.createElement("textarea");
      const saveButton = document.createElement("button");
      const smallText = document.createElement("small");

      textArea.classList.add(
        "form-control",
        "border-0",
        "mb-3",
        "mt-3",
        "bg-primay",
        "bg-opacity-10",
      );
      textArea.textContent = postPara.textContent;
      postPara.replaceWith(textArea);
      textArea.select();

      saveButton.classList.add(
        "btn",
        "btn-white",
        "border",
        "text-gray",
        "btn-small",
      );
      smallText.classList.add("text-muted");
      smallText.textContent = "Save";
      saveButton.appendChild(smallText);
      btn.replaceWith(saveButton);

      saveButton.onclick = () => {
        if (textArea.value.length < 1 || textArea.value.length > 255) {
          saveButton.replaceWith(btn);
          textArea.replaceWith(postPara);
          return;
        }
        fetch(`edit/${btn.dataset.id}`, {
          method: "POST",
          body: JSON.stringify({ content: textArea.value }),
        })
          .then((res) => res.json())
          .then((data) => {
            saveButton.replaceWith(btn);
            postPara.textContent = data.content;
            textArea.replaceWith(postPara);
          });
      };
    };
  });
};

const likes = () => {
  const allPosts = document.querySelectorAll(".like-button");

  allPosts.forEach((post) => {
    fetch(`/likes/${post.dataset.id}`)
      .then((res) => res.json())
      .then((data) => {
        displayLikes(post, data);
        setLikesListener(post);
      });
  });
};

const displayLikes = (post, data) => {
  post.querySelector(".display-likes").innerText = data.likes.length;
};

const setLikesListener = (post) => {
  post.onclick = () => {
    fetch(`/like/${post.dataset.id}`, { method: "POST" })
      .then((res) => res.json())
      .then((data) =>
        fetch(`/likes/${post.dataset.id}`)
          .then((res) => res.json())
          .then((data) => displayLikes(post, data)),
      );
  };
};

init();
