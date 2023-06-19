const init = () => {
  document.addEventListener("DOMContentLoaded", () => {
    likes();
    createNewPost();
  });
};

const createNewPost = () => {
  const newPost = document.querySelector("#newPost");
  const newPostButton = document.querySelector("#newPostButton");

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

const likes = () => {
  document.querySelectorAll(".like-button").forEach((post) => {
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
