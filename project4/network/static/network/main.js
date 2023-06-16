const init = () => {
  document.addEventListener("DOMContentLoaded", () => {
    createNewPost();
    displayPosts();
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
      .then((data) => data.message && (newPost.value = ""));
  };
};

const displayPosts = () => {
  const allPosts = document.querySelector("#allPosts");
  fetch("/posts")
    .then((res) => res.json())
    .then((data) => {
      console.log(data);
    });
};

init();
