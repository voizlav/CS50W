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
      .then((data) => displayMessage(...Object.entries(data)[0]));
  };
};

const displayMessage = (type, message) => {
  /* TODO */
  console.log("Type:", type);
  console.log("Msg:", message);
};

init();
