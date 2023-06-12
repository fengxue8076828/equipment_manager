function enableUserEdit() {
  inputs = document.querySelectorAll("input");
  changePhotoBtn = document.getElementById("change-photo-btn");
  changePhotoBtn.removeAttribute("hidden");
  submitBtn = document.getElementById("submit");
  submitBtn.classList.remove("hide");
  inputs.forEach(function (input) {
    input.removeAttribute("disabled");
  });
}

function updateUser(e) {
  e.preventDefault();
  form = document.getElementById("user-form");
  data = new FormData(form);
  const xhr = new XMLHttpRequest();
  xhr.open("POST", "user-profile/", true);
  xhr.onload = function () {
    if (this.status == 200) {
      const contentText = JSON.parse(this.responseText);
      if (contentText.message == "success") {
        alert("更新成功！");
        const xhr1 = new XMLHttpRequest();
        mainContent = document.getElementById("main-content");
        xhr1.open("GET", "user-profile/", true);
        xhr1.onload = function () {
          if (this.status == 200) {
            const contentText = JSON.parse(this.responseText);
            mainContent.innerHTML = contentText.content;
            inputs = document.querySelectorAll("input");
            inputs.forEach(function (input) {
              input.setAttribute("disabled", "");
            });
            setTimeout(function () {
              successMessage = document.getElementById("success");
              successMessage.classList.add("hide");
            }, 3000);
            document.getElementById("photo").src = document.getElementById(
              "profile-title-image"
            ).src;
            document.getElementById("real-name").textContent =
              document.getElementById("id_real_name").value;
            document.getElementById("email").textContent =
              document.getElementById("id_email").value;
            document.getElementById("cellphone-number").textContent =
              document.getElementById("id_cellphone_number").value;
          }
        };
        xhr1.send();
      }
    }
  };
  xhr.send(data);
}

function updateUserPassword() {
  const mainContent = document.getElementById("main-content");
  const xhr = new XMLHttpRequest();
  xhr.open("GET", "user-password/", true);
  xhr.onload = function () {
    if (this.status === 200) {
      const responseText = JSON.parse(this.responseText);
      content = responseText.content;
      mainContent.innerHTML = content;
    }
  };
  xhr.send();
}
function updateUserPasswordSubmit(e) {
  e.preventDefault();
  const mainContent = document.getElementById("main-content");
  form = document.getElementById("password-form");
  data = new FormData(form);
  xhr = new XMLHttpRequest();
  xhr.open("POST", "user-password/", true);
  xhr.onload = function () {
    if (this.status === 200) {
      const responseText = JSON.parse(this.responseText);
      if (responseText.message) {
        window.location.href = "logout/";
      } else {
        content = responseText.content;
        mainContent.innerHTML = content;
      }
    }
  };
  xhr.send(data);
}

function changePhoto() {
  realBtn = document.getElementById("id_photo");
  console.log(realBtn);
  realBtn.click();
}

function previewPhoto(e) {
  image = document.getElementById("profile-title-image");
  fileBtn = document.getElementById("id_photo");
  if (fileBtn.files) {
    const [file] = fileBtn.files;
    image.src = URL.createObjectURL(file);
  }
}
