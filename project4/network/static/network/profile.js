const profile = () => {
  const followButton = document.querySelector("#follow-button");
  if (followButton) followButton.onclick = () => followProfile(followButton);
};

const followProfile = (btn) =>
  fetch(`/follow/${btn.dataset.id}`, { method: "POST" }).then(() =>
    displayProfileData(btn),
  );

const displayProfileData = (btn) => {
  const following = document.querySelector("#following");
  const followers = document.querySelector("#followers");

  fetch(`/profile/${btn.dataset.username}`, { method: "POST" })
    .then((res) => res.json())
    .then((data) => {
      following.textContent = `${data.following} Following`;
      followers.textContent = `${data.followers} Followers`;
      data.is_followed
        ? (btn.textContent = "Unfollow")
        : (btn.textContent = "Follow");
    });
};

profile();
