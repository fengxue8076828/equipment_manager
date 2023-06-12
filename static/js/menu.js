window.addEventListener("load", initialPage);

function gotoLink(link) {
  const mainContent = document.getElementById("main-content");
  const xhr = new XMLHttpRequest();
  xhr.open("GET", link, true);
  xhr.onload = function () {
    if (this.status === 200) {
      const responseText = JSON.parse(this.responseText);
      content = responseText.content;
      mainContent.innerHTML = content;
    }
  };
  xhr.send();
}

function initialPage() {
  getMenu();
  getOutboundPayList();
}

function renderMenu(parent_module, menus) {
  let menuHTML = "";
  let items = menus.filter(function (menu) {
    return menu.fields.parent_module == parent_module;
  });
  for (let item of items) {
    menuHTML += renderMenuItem(item);
    menuHTML += renderMenu(item.pk, menus);
  }
  return menuHTML;
}

function renderMenuItem(item) {
  let menuItemHTML = "";
  if (!item.fields.parent_module) {
    menuItemHTML = `
            <div class="menu-item" id="${item.pk}">
                <div class="menu-item-title">
                    ${item.fields.icon}
                    <h4>${item.fields.name}</h4>
                </div>
                <i class="fa-solid fa-caret-right"></i>
            </div>
        `;
  } else {
    menuItemHTML = `
        <div class="menu-item menu-second hide" id="${item.pk}" data-parent="${item.fields.parent_module}">
            <div class="menu-item-title"  onclick="gotoLink('${item.fields.link}')">
                ${item.fields.icon}
                <h5>${item.fields.name}</h5>
            </div>
            <i class="fa-solid fa-caret-right"></i>
        </div>
    `;
  }
  return menuItemHTML;
}

function getMenu() {
  const menuContainer = document.getElementById("menu-items");
  let menuHTML = "";
  const xhr = new XMLHttpRequest();
  xhr.open("GET", "menu/", true);
  xhr.onload = function () {
    if (this.status === 200) {
      const responseText = JSON.parse(this.responseText);
      let menuItems = JSON.parse(responseText.menu);
      menuContainer.innerHTML = renderMenu(null, menuItems);
    }
  };
  xhr.send();
}
function getOutboundPayList() {
  const mainContent = document.getElementById("main-content");
  const xhr = new XMLHttpRequest();
  xhr.open("GET", `postsale/outbound-pay-list/`, true);
  xhr.onload = function () {
    if (this.status === 200) {
      const responseText = JSON.parse(this.responseText);
      content = responseText.content;
      mainContent.innerHTML = content;
    }
  };
  xhr.send();
}
document.addEventListener("click", function (e) {
  if (
    (e.target.classList.contains("menu-item") && !e.target.dataset.parent) ||
    (e.target.closest(".menu-item") &&
      !e.target.closest(".menu-item").dataset.parent)
  ) {
    secondItems = document.querySelectorAll("[data-parent]");
    secondItems.forEach(function (item) {
      item.classList.remove("hide");
      if (
        item.dataset.parent !=
        (e.target.classList.contains("menu-item")
          ? e.target.id
          : e.target.closest(".menu-item").id)
      ) {
        item.classList.add("hide");
      }
    });
  }
});

document.getElementById("photo").addEventListener("click", function () {
  const xhr = new XMLHttpRequest();
  mainContent = document.getElementById("main-content");
  xhr.open("GET", "user-profile/", true);
  xhr.onload = function () {
    if (this.status == 200) {
      const contentText = JSON.parse(this.responseText);
      mainContent.innerHTML = contentText.content;
      inputs = document.querySelectorAll("input");
      inputs.forEach(function (input) {
        input.setAttribute("disabled", "");
      });
    }
  };
  xhr.send();
});

function gotoPage(e, url, page) {
  if (url.endsWith("/")) {
    url = `${url}?page=${page}`;
  } else {
    url = `${url}&page=${page}`;
  }

  gotoLink(url);
}
