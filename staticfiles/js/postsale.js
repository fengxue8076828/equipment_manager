function toOutbound() {
  devices = document.getElementById("selected-device").value.trim(",");
  if (!devices) {
    alert("请选择出库设备！");
    return;
  }
  const mainContent = document.getElementById("main-content");
  const xhr = new XMLHttpRequest();
  xhr.open("GET", `postsale/device-sold-create/?devices=${devices}`, true);
  xhr.onload = function () {
    if (this.status === 200) {
      const responseText = JSON.parse(this.responseText);
      content = responseText.content;
      mainContent.innerHTML = content;
    }
  };
  xhr.send();
}

function outbound(e) {
  if (!document.getElementById("id_buyer").value) {
    alert("请选择客户！");
    return;
  }

  buyer = document.getElementById("id_buyer").value;
  const devices = document.querySelectorAll("[data-id]");
  const devicesIds = [];

  for (let device of devices) {
    devicesIds.push(device.dataset.id);
  }
  const devicesIdsStr = devicesIds.join(",");

  xhr = new XMLHttpRequest();
  xhr.responseType = "blob";
  xhr.open(
    "GET",
    `postsale/outbound-file/?devices=${devicesIdsStr}&buyer=${buyer}`,
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
}

function deviceSoldCreateSubmit(e) {
  e.preventDefault();

  const devices = document.querySelectorAll("[data-id]");
  const devicesIds = [];
  for (let device of devices) {
    devicesIds.push(device.dataset.id);
  }
  const devicesIdsStr = devicesIds.join(",");

  form = document.getElementById("device-sold-create-form");
  data = new FormData(form);
  xhr = new XMLHttpRequest();
  xhr.open(
    "POST",
    `postsale/device-sold-update/?devices=${devicesIdsStr}`,
    true
  );
  xhr.onload = function () {
    if (this.status === 200) {
      alert("出库成功！");
      gotoLink("/postsale/device-forsale-list/");
    }
  };
  xhr.send(data);
}

function outboundList() {
  const beginDate = document.getElementById("begin-date").value;
  const endDate = document.getElementById("end-date").value;
  const payState = document.getElementById("pay-state").value;

  const mainContent = document.getElementById("main-content");
  const xhr = new XMLHttpRequest();
  xhr.open(
    "GET",
    `postsale/outbound-list/?pay_state=${payState}&begin_date=${beginDate}&end_date=${endDate}`,
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

function soldDeviceList(e) {
  const outboundId = e.target.dataset.id;
  const mainContent = document.getElementById("main-content");
  const xhr = new XMLHttpRequest();
  xhr.open("GET", `postsale/device-sold-list/?outbound_id=${outboundId}`, true);
  xhr.onload = function () {
    if (this.status === 200) {
      const responseText = JSON.parse(this.responseText);
      content = responseText.content;
      mainContent.innerHTML = content;
    }
  };
  xhr.send();
}

function searchSoldDevice(e) {
  const equipmentName = document.querySelector("#equipment-name").value;
  const buyer = document.querySelector("#buyer").value;
  const fixAddress = document.querySelector("#fix-address").value;
  const state = document.querySelector("#state").value;
  const mainContent = document.getElementById("main-content");

  xhr = new XMLHttpRequest();
  xhr.open(
    "GET",
    `postsale/device-sold-list/?equipment_name=${equipmentName}&buyer=${buyer}&fix_address=${fixAddress}&state=${state}`,
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

function enable(e) {
  e.target.removeAttribute("disabled");
}

function updateSoldDevice(e) {
  const soldDeviceId = e.target.closest("tr").dataset.id;

  const fixAddress = document.querySelector(
    `[data-id='${soldDeviceId}'] input[name='fix-address']`
  ).value;
  const maintainer = document.querySelector(
    `[data-id='${soldDeviceId}'] select[name='maintainer']`
  ).value;

  const data = new FormData();
  data.append("maintainer", maintainer);
  data.append("fix_address", fixAddress);

  const xhr = new XMLHttpRequest();
  xhr.open("POST", `postsale/device-sold-modify/${soldDeviceId}/`);
  xhr.onload = function () {
    if (this.status === 200) {
      alert("更新成功！");
    }
  };
  xhr.send(data);
}

function outboundFile(e) {
  const id = e.target.dataset.id;
}

function getOutboundPayListByDays() {
  const days = document.getElementById("overdue_days").value;
  console.log(days);
  const mainContent = document.getElementById("main-content");
  const xhr = new XMLHttpRequest();
  xhr.open("GET", `postsale/outbound-pay-list/?days=${days}`, true);
  xhr.onload = function () {
    if (this.status === 200) {
      const responseText = JSON.parse(this.responseText);
      content = responseText.content;
      mainContent.innerHTML = content;
    }
  };
  xhr.send();
}

function clientCreate(e) {
  const mainContent = document.getElementById("main-content");

  xhr = new XMLHttpRequest();
  xhr.open("GET", `postsale/client-create/`, true);
  xhr.onload = function () {
    if (this.status === 200) {
      const responseText = JSON.parse(this.responseText);
      content = responseText.content;
      mainContent.innerHTML = content;
    }
  };
  xhr.send();
}

function clientCreateSubmit(e) {
  e.preventDefault();
  form = document.getElementById("client-create-form");
  data = new FormData(form);
  xhr = new XMLHttpRequest();
  xhr.open("POST", `postsale/client-create/`, true);
  xhr.onload = function () {
    if (this.status === 200) {
      alert("添加成功！");
      gotoLink("postsale/client-list/");
    }
  };
  xhr.send(data);
}

function clientUpdate(e) {
  const mainContent = document.getElementById("main-content");
  const clientId = e.target.closest("tr").dataset.id;
  xhr = new XMLHttpRequest();
  xhr.open("GET", `postsale/client-update/${clientId}/`, true);
  xhr.onload = function () {
    if (this.status === 200) {
      const responseText = JSON.parse(this.responseText);
      content = responseText.content;
      mainContent.innerHTML = content;
    }
  };
  xhr.send();
}

function clientUpdateSubmit(e) {
  e.preventDefault();
  const clientId = e.target.dataset.id;
  data = new FormData(e.target);
  xhr = new XMLHttpRequest();
  xhr.open("POST", `postsale/client-update/${clientId}/`, true);
  xhr.onload = function () {
    if (this.status === 200) {
      const res = JSON.parse(this.responseText);
      alert("更新成功");
      gotoLink("postsale/client-list/");
    }
  };
  xhr.send(data);
}

function searchClient() {
  const client = document.querySelector("#client-name").value;
  const mainContent = document.getElementById("main-content");

  xhr = new XMLHttpRequest();
  xhr.open("GET", `postsale/client-list/?name=${client}`, true);
  xhr.onload = function () {
    if (this.status === 200) {
      const responseText = JSON.parse(this.responseText);
      content = responseText.content;
      mainContent.innerHTML = content;
    }
  };
  xhr.send();
}

function clientDelete(e) {
  if (confirm("确实要删除该客户吗？")) {
    const clientId = e.target.closest("tr").dataset.id;
    const xhr = new XMLHttpRequest();
    xhr.open("POST", `postsale/client-delete/${clientId}`, true);
    xhr.onload = function () {
      if (this.status === 200) {
        const res = JSON.parse(this.responseText);
        if (res.message == "not-empty") {
          alert("该客户有出库记录，不能删除！");
        } else {
          alert("删除成功！");
          gotoLink("postsale/client-list/");
        }
      }
    };
    xhr.send();
  }
}

function toggleDevice(e) {
  const selectedDevice = document.getElementById("selected-device");
  const deviceId = e.target.value;
  if (selectedDevice.value.includes(deviceId)) {
    selectedDevice.value = selectedDevice.value.replace(deviceId + ",", "");
  } else {
    selectedDevice.value += deviceId + ",";
  }
}

function backToOutboundList() {
  gotoLink("postsale/outbound-list/");
}

function enableDeviceEdit(element) {
  console.log(element.querySelector("input"));
  element.querySelector("input").disabled = false;
  element.querySelector("select").disabled = false;
}

function disableDeviceEdit(element) {
  element.querySelector("input").disabled = true;
  element.querySelector("select").disabled = true;
}
