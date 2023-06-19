const init = () => {
  document.addEventListener("DOMContentLoaded", () => {
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

init();
