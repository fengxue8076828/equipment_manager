function equipmentCreate() {
  const mainContent = document.getElementById("main-content");
  const xhr = new XMLHttpRequest();
  xhr.open("GET", "presale/equipment-create/", true);
  xhr.onload = function () {
    if (this.status === 200) {
      const responseText = JSON.parse(this.responseText);
      content = responseText.content;
      mainContent.innerHTML = content;
    }
  };
  xhr.send();
}

function equipmentCreateSubmit(e) {
  e.preventDefault();

  form = document.getElementById("equipment-create-form");
  data = new FormData(form);
  xhr = new XMLHttpRequest();
  xhr.open("POST", "presale/equipment-create/", true);
  xhr.onload = function () {
    if (this.status === 200) {
      gotoLink("presale/equipment-list/");
    }
  };
  xhr.send(data);
}

function getEquipment(e) {
  equipment_id = e.target.value;
  if (equipment_id != "") {
    xhr = new XMLHttpRequest();
    xhr.open("GET", `presale/equipment-detail/${equipment_id}`, true);
    xhr.onload = function () {
      if (this.status === 200) {
        const res = JSON.parse(this.responseText);
        const data = JSON.parse(res.data)[0];
        console.log(data);
        ec = document.getElementById("equipment-container");
        ec.querySelector("#name").textContent = data.fields.name;
        ec.querySelector("#model").textContent = data.fields.model;
        ec.querySelector("#hardware_serial").textContent =
          data.fields.hardware_serial;
        ec.querySelector("#software_serial").textContent =
          data.fields.software_serial;
      }
    };
    xhr.send();
  }
}

function inbound(e) {
  const warehouse_id = document.getElementById("id_warehouse").value;
  const equipment_id = document.getElementById("id_equipment").value;
  const amount = document.getElementById("id_amount").value * 1;
  const supplier_id = document.getElementById("id_supplier").value;
  if (equipment_id && warehouse_id && supplier_id && amount > 0) {
    xhr = new XMLHttpRequest();
    xhr.responseType = "blob";
    xhr.open(
      "GET",
      `presale/inbound-file/${equipment_id}/${warehouse_id}/${amount}/${supplier_id}/`,
      true
    );
    xhr.onload = function () {
      var url = URL.createObjectURL(xhr.response);
      var link = document.createElement("a");
      link.href = url;
      link.target = "_blank";
      link.click();
    };
    xhr.send();
  } else {
    alert("信息有误，请检查！");
  }
}

function inboundCreateSubmit(e) {
  e.preventDefault();
  form = document.getElementById("inbound-create-form");
  data = new FormData(form);
  xhr = new XMLHttpRequest();
  xhr.open("POST", `presale/inbound-create/`, true);
  xhr.onload = function () {
    if (this.status === 200) {
      gotoLink("presale/equipment-list/");
    }
  };
  xhr.send(data);
}

function updateEquipment(e) {
  const equipmentId = e.target.closest("tr").dataset.id;
  const mainContent = document.getElementById("main-content");
  const xhr = new XMLHttpRequest();
  xhr.open("GET", `presale/equipment-update/${equipmentId}`, true);
  xhr.onload = function () {
    if (this.status === 200) {
      const responseText = JSON.parse(this.responseText);
      content = responseText.content;
      mainContent.innerHTML = content;
    }
  };
  xhr.send();
}

function updateEquipmentSubmit(e) {
  e.preventDefault();
  form = document.getElementById("equipment-update-form");
  equipmentId = form.dataset.id;
  data = new FormData(form);
  xhr = new XMLHttpRequest();
  xhr.open("POST", `presale/equipment-update/${equipmentId}/`, true);
  xhr.onload = function () {
    if (this.status === 200) {
      gotoLink("presale/equipment-list/");
    }
  };
  xhr.send(data);
}

function deleteEquipment(e) {
  if (confirm("确实要删除该设备？")) {
    const equipmentId = e.target.closest("tr").dataset.id;
    const mainContent = document.getElementById("main-content");
    const xhr = new XMLHttpRequest();
    xhr.open("POST", `presale/equipment-delete/${equipmentId}`, true);
    xhr.onload = function () {
      if (this.status === 200) {
        const res = JSON.parse(this.responseText);
        if (res.message == "not-empty") {
          alert("库存中还有设备，不能删除！");
        } else {
          alert("删除成功！");
          gotoLink("presale/equipment-list/");
        }
      }
    };
    xhr.send();
  }
}

function listDevice(e) {
  const equipmentId = e.target.closest("tr").dataset.id;
  const mainContent = document.getElementById("main-content");
  const xhr = new XMLHttpRequest();
  xhr.open("GET", `presale/device-list/${equipmentId}/`, true);
  xhr.onload = function () {
    if (this.status === 200) {
      const responseText = JSON.parse(this.responseText);
      content = responseText.content;
      mainContent.innerHTML = content;
    }
  };
  xhr.send();
}

function checkDevice(e) {
  const deviceId = e.target.closest("tr").dataset.id;
  const mainContent = document.getElementById("main-content");
  xhr = new XMLHttpRequest();
  xhr.open(
    "GET",
    `presale/device-update/${deviceId}/?back=${
      document.getElementById("current_url").value
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
function deviceUpdateSubmit(e) {
  e.preventDefault();
  const deviceId = e.target.dataset.id;
  data = new FormData(e.target);
  xhr = new XMLHttpRequest();
  xhr.open("POST", `presale/device-update/${deviceId}/`, true);
  xhr.onload = function () {
    if (this.status === 200) {
      const res = JSON.parse(this.responseText);
      if (res.message == "success") {
        alert("更新成功");
      } else {
        alert("更新失败！");
      }
    }
  };
  xhr.send(data);
}

function searchSupplier() {
  const supplier = document.querySelector("#supplier-name").value;
  const mainContent = document.getElementById("main-content");

  xhr = new XMLHttpRequest();
  xhr.open("GET", `presale/supplier-list/?name=${supplier}`, true);
  xhr.onload = function () {
    if (this.status === 200) {
      const responseText = JSON.parse(this.responseText);
      content = responseText.content;
      mainContent.innerHTML = content;
    }
  };
  xhr.send();
}

function supplierCreate() {
  const mainContent = document.getElementById("main-content");

  xhr = new XMLHttpRequest();
  xhr.open("GET", `presale/supplier-create/`, true);
  xhr.onload = function () {
    if (this.status === 200) {
      const responseText = JSON.parse(this.responseText);
      content = responseText.content;
      mainContent.innerHTML = content;
    }
  };
  xhr.send();
}
function supplierCreateSubmit(e) {
  e.preventDefault();
  form = document.getElementById("supplier-create-form");
  data = new FormData(form);
  xhr = new XMLHttpRequest();
  xhr.open("POST", `presale/supplier-create/`, true);
  xhr.onload = function () {
    if (this.status === 200) {
      alert("添加成功！");
      gotoLink("presale/supplier-list/");
    }
  };
  xhr.send(data);
}
function supplierUpdate(e) {
  const mainContent = document.getElementById("main-content");
  const supplierId = e.target.closest("tr").dataset.id;
  xhr = new XMLHttpRequest();
  xhr.open("GET", `presale/supplier-update/${supplierId}/`, true);
  xhr.onload = function () {
    if (this.status === 200) {
      const responseText = JSON.parse(this.responseText);
      content = responseText.content;
      mainContent.innerHTML = content;
    }
  };
  xhr.send();
}
function supplierUpdateSubmit(e) {
  e.preventDefault();
  const supplierId = e.target.dataset.id;
  data = new FormData(e.target);
  xhr = new XMLHttpRequest();
  xhr.open("POST", `presale/supplier-update/${supplierId}/`, true);
  xhr.onload = function () {
    if (this.status === 200) {
      const res = JSON.parse(this.responseText);
      alert("更新成功");
      gotoLink("presale/supplier-list/");
    }
  };
  xhr.send(data);
}

function supplierDelete(e) {
  if (confirm("确实要删除该供货商吗？")) {
    const supplierId = e.target.closest("tr").dataset.id;
    const mainContent = document.getElementById("main-content");
    const xhr = new XMLHttpRequest();
    xhr.open("POST", `presale/supplier-delete/${supplierId}`, true);
    xhr.onload = function () {
      if (this.status === 200) {
        const res = JSON.parse(this.responseText);
        if (res.message == "not-empty") {
          alert("还有该供货商的设备，不能删除！");
        } else {
          alert("删除成功！");
          gotoLink("presale/supplier-list/");
        }
      }
    };
    xhr.send();
  }
}
function backToEquipmentList() {
  gotoLink("presale/equipment-list/");
}

function goBack() {
  const url = document.getElementById("back-url").value;
  console.log(url)
  gotoLink(url);
}
