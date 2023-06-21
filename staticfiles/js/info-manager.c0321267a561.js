function userCreate() {
  const mainContent = document.getElementById("main-content");
  const xhr = new XMLHttpRequest();
  xhr.open("GET", "info-manager/user-create/", true);
  xhr.onload = function () {
    if (this.status === 200) {
      const responseText = JSON.parse(this.responseText);
      content = responseText.content;
      mainContent.innerHTML = content;
    }
  };
  xhr.send();
}

function passwordReset(e) {
  if (!confirm("确定要重置密码吗？")) {
    return false;
  }
  id = e.target.dataset.id;
  const xhr = new XMLHttpRequest();
  xhr.open("GET", `info-manager/reset-password/${id}/`, true);
  xhr.onload = function () {
    if (this.status === 200) {
      alert("密码重置成功！");
    }
  };
  xhr.send();
}
function userCreateSubmit(e) {
  e.preventDefault();
  const mainContent = document.getElementById("main-content");
  form = document.getElementById("user-create-form");
  data = new FormData(form);
  xhr = new XMLHttpRequest();
  xhr.open("POST", "info-manager/user-create/", true);
  xhr.onload = function () {
    if (this.status === 200) {
      console.log("hello");
      const responseText = JSON.parse(this.responseText);
      content = responseText.content;
      mainContent.innerHTML = content;
      const success_span = document.getElementById("success");
      console.log(success_span);
      setTimeout(() => {
        success_span.style.display = "none";
      }, 2000);
    }
  };
  xhr.send(data);
}

function userDelete(e) {
  if (confirm("确定要删除用户吗？")) {
    id = e.target.dataset.id;
    const mainContent = document.getElementById("main-content");
    const xhr = new XMLHttpRequest();
    xhr.open(
      "GET",
      `info-manager/user-delete/${id}/${
        document.getElementById("roles").value
      }`,
      true
    );
    xhr.onload = function () {
      if (this.status === 200) {
        const responseText = JSON.parse(this.responseText);
        content = responseText.content;
        mainContent.innerHTML = content;
      }
    };
    xhr.send();
  }
}

function filterUsers() {
  link = "info-manager/user-list/" + document.getElementById("roles").value;
  gotoLink(link);
}

function addModule(e) {
  const formList = document.getElementById("from-list");
  const toList = document.getElementById("to-list");
  moduleId = e.target.dataset.moduleId;
  parentModuleId = e.target.dataset.parentModuleId;

  if (!toList.querySelector(`[data-module-id='${moduleId}']`)) {
    element = e.target.cloneNode(true);
    element.setAttribute("ondblclick", "removeModule(event)");
    parent = toList.querySelector(`[data-module-id='${parentModuleId}']`);
    if (!parent) {
      parent = from.querySelector(`[data-module-id='${parentModuleId}']`);
      toList.appendChild(parent);
    }
    insertAfter(parent, element);
  }
}

function removeModule(e) {
  const toList = document.getElementById("to-list");
  toList.removeChild(e.target);
}
function updateRole() {
  const toList = document.getElementById("to-list");
  const roleId = document.getElementById("role-list").value;
  if (toList.children.length > 0) {
    const selectedModules = [...toList.children].map(
      (child) => child.dataset.moduleId
    );
    const data = new FormData();
    data.append("role_id", roleId);
    data.append("modules", selectedModules);
    xhr = new XMLHttpRequest();
    xhr.open("POST", "info-manager/role-update/", true);
    xhr.onload = function () {
      if (this.status === 200) {
        alert("更新成功！");
        const responseText = JSON.parse(this.responseText);
        content = responseText.content;
        mainContent.innerHTML = content;
      }
    };
    xhr.send(data);
  }
}

function getRoleModules(e) {
  const mainContent = document.getElementById("main-content");
  const roleId = document.getElementById("role-list").value;
  const xhr = new XMLHttpRequest();
  xhr.open("GET", `info-manager/role-list/?role_id=${roleId}`, true);
  xhr.onload = function () {
    if (this.status === 200) {
      const responseText = JSON.parse(this.responseText);
      content = responseText.content;
      mainContent.innerHTML = content;
    }
  };
  xhr.send();
}

function insertAfter(referenceNode, newNode) {
  referenceNode.parentNode.insertBefore(newNode, referenceNode.nextSibling);
}

function toggle(e) {
  if (e.target.textContent == "展开二级类别") {
    e.target.textContent = "收起二级类别";

    categoryId = e.target.closest("tr").dataset.id;
    const xhr = new XMLHttpRequest();
    xhr.open("GET", `info-manager/category-list/${categoryId}/`);
    xhr.onload = function () {
      if (this.status === 200) {
        const responseText = JSON.parse(this.responseText);
        content = responseText.content;
        const node = new DOMParser().parseFromString(content, "text/html");
        const parent_tr = e.target.closest("tr");
        node.querySelectorAll("tr").forEach((element) => {
          parent_tr.after(element);
        });
      }
    };
    xhr.send();
  } else {
    e.target.textContent = "展开二级类别";
    categoryId = e.target.closest("tr").dataset.id;
    const tableElement = e.target.closest("tbody");
    console.log(tableElement);
    tableElement
      .querySelectorAll(`[data-parent-id='${categoryId}']`)
      .forEach((el) => {
        tableElement.removeChild(el);
      });
  }
}
function updateCategory(e) {
  console.log(e.target.closest("tr"));
  categoryId = e.target.closest("tr").dataset.id;

  const name = document.querySelector(
    `[data-id='${categoryId}'] input[name='name']`
  ).value;
  const description = document.querySelector(
    `[data-id='${categoryId}'] input[name='description']`
  ).value;

  const data = new FormData();
  data.append("name", name);
  data.append("description", description);

  const xhr = new XMLHttpRequest();
  xhr.open("POST", `info-manager/category-update/${categoryId}/`);
  xhr.onload = function () {
    if (this.status == 200) {
      alert("修改成功！");
    }
  };
  xhr.send(data);
}

function deleteCategory(e) {
  if (!confirm("确实要删除该目录吗?")) {
    return;
  }
  categoryId = e.target.closest("tr").dataset.id;
  const xhr = new XMLHttpRequest();
  xhr.open("POST", `info-manager/category-delete/${categoryId}/`);
  xhr.onload = function () {
    if (this.status === 200) {
      const responseText = JSON.parse(this.responseText);
      const message = responseText.message;
      if (message == "has-children") {
        alert("该目录下还有子目录，不能删除！");
        return;
      }
      if (message == "has-equipments") {
        alert("该目录下还有设备，不能删除！");
        return;
      }
      e.target.closest("tr").remove();
    }
  };
  xhr.send();
}

function enableEdit(e) {
  e.target.removeAttribute("readonly");
}
function disableEdit(e) {
  e.target.setAttribute("readonly", "");
}

function categoryCreate() {
  const mainContent = document.getElementById("main-content");
  const xhr = new XMLHttpRequest();
  xhr.open("GET", "info-manager/category-create/", true);
  xhr.onload = function () {
    if (this.status === 200) {
      const responseText = JSON.parse(this.responseText);
      content = responseText.content;
      mainContent.innerHTML = content;
    }
  };
  xhr.send();
}

function categoryCreateSubmit(e) {
  e.preventDefault();

  form = document.getElementById("category-create-form");
  data = new FormData(form);
  xhr = new XMLHttpRequest();
  xhr.open("POST", "info-manager/category-create/", true);
  xhr.onload = function () {
    if (this.status === 200) {
      gotoLink("info-manager/category-list/");
    }
  };
  xhr.send(data);
}

function warehouseCreate() {
  const mainContent = document.getElementById("main-content");
  const xhr = new XMLHttpRequest();
  xhr.open("GET", "info-manager/warehouse-create/", true);
  xhr.onload = function () {
    if (this.status === 200) {
      const responseText = JSON.parse(this.responseText);
      content = responseText.content;
      mainContent.innerHTML = content;
    }
  };
  xhr.send();
}

function warehouseCreateSubmit(e) {
  e.preventDefault();

  form = document.getElementById("warehouse-create-form");
  data = new FormData(form);
  xhr = new XMLHttpRequest();
  xhr.open("POST", "info-manager/warehouse-create/", true);
  xhr.onload = function () {
    if (this.status === 200) {
      gotoLink("info-manager/warehouse-list/");
    }
  };
  xhr.send(data);
}

function updateWarehouse(e) {
  warehouseId = e.target.closest("tr").dataset.id;

  const number = document.querySelector(
    `[data-id='${warehouseId}'] input[name='number']`
  ).value;
  const name = document.querySelector(
    `[data-id='${warehouseId}'] input[name='name']`
  ).value;
  const location = document.querySelector(
    `[data-id='${warehouseId}'] input[name='location']`
  ).value;
  const description = document.querySelector(
    `[data-id='${warehouseId}'] input[name='description']`
  ).value;

  const data = new FormData();
  data.append("number", number);
  data.append("name", name);
  data.append("location", location);
  data.append("description", description);

  const xhr = new XMLHttpRequest();
  xhr.open("POST", `info-manager/warehouse-update/${warehouseId}/`);
  xhr.onload = function () {
    if (this.status == 200) {
      alert("修改成功！");
    }
  };
  xhr.send(data);
}

function deleteWarehouse(e) {
  if (!confirm("确实要删除仓库吗？")) {
    return false;
  }
  warehouseId = e.target.closest("tr").dataset.id;
  const xhr = new XMLHttpRequest();
  xhr.open("POST", `info-manager/warehouse-delete/${warehouseId}/`);
  xhr.onload = function () {
    if (this.status === 200) {
      const responseText = JSON.parse(this.responseText);
      if (responseText.message == "has-devices") {
        alert("该仓库还有设备，不能删除！");
        return;
      }
      e.target.closest("tr").remove();
    }
  };
  xhr.send();
}

function deviceListByWarehouse(e) {
  const mainContent = document.getElementById("main-content");
  warehouseId = e.target.closest("tr").dataset.id;
  const xhr = new XMLHttpRequest();
  xhr.open("GET", `presale/device-list-by-warehouse/${warehouseId}/`);
  xhr.onload = function () {
    if (this.status === 200) {
      const responseText = JSON.parse(this.responseText);
      content = responseText.content;
      mainContent.innerHTML = content;
    }
  };
  xhr.send();
}
function warehouseList() {
  gotoLink("info-manager/warehouse-list/");
}
