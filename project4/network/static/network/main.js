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
  allPosts.classList.add("mt-5");
  fetch("/posts")
    .then((res) => res.json())
    .then((data) => {
      console.log(data);
      const listOfPosts = document.createElement("div");
      listOfPosts.classList.add("list-group");
      data.forEach((post) => {
        console.log(post);
        const listGroupPost = document.createElement("a");
        listGroupPost.classList.add(
          "list-group-item",
          "list-group-item-action",
        );
        const divWrapper = document.createElement("div");
        divWrapper.classList.add(
          "d-flex",
          "w-100",
          "justify-content-between",
          "pb-3",
        );
      });
    });
};

init();
