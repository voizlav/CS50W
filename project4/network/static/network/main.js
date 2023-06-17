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
      .then((data) => {
        if (data.message) {
          newPost.value = "";
          displayPosts();
        }
      });
  };
};

const displayPosts = () => {
  const allPosts = document.querySelector("#allPosts");
  allPosts.classList.add("mt-5");
  allPosts.innerHTML = "";

  fetch("/posts")
    .then((res) => res.json())
    .then((data) => {
      const listOfPosts = document.createElement("div");
      listOfPosts.classList.add("list-group");
      data.forEach((post) => listOfPosts.appendChild(createPostElements(post)));
      allPosts.appendChild(listOfPosts);
    });
};

const createPostElements = (post) => {
  const listGroupPost = document.createElement("a");
  listGroupPost.classList.add("list-group-item", "list-group-item-action");

  const divWrapper = document.createElement("div");
  divWrapper.classList.add(
    "d-flex",
    "w-100",
    "justify-content-between",
    "pb-3",
  );
  const postHeading = document.createElement("h5");
  postHeading.classList.add("mb-1");
  postHeading.innerText = post.user;

  const timestamp = document.createElement("small");
  timestamp.classList.add("text-muted");
  timestamp.innerText = post.timestamp;

  const postContent = document.createElement("p");
  postContent.classList.add("mb-1", "text-break");
  postContent.innerText = post.content;

  listGroupPost.appendChild(divWrapper);
  divWrapper.appendChild(postHeading);
  divWrapper.appendChild(timestamp);
  listGroupPost.appendChild(postContent);

  // TODO: Add likes
  return listGroupPost;
};

init();
