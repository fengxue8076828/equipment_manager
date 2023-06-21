function searchDevice() {
  const deviceName = document.querySelector("#maintainance-device-name").value;
  const type = document.getElementById("type").value;
  const mainContent = document.getElementById("main-content");

  xhr = new XMLHttpRequest();
  xhr.open(
    "GET",
    `maintainance/device-list/${type}/?device_name=${deviceName}`,
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
function dispatchDevice(e) {
  deviceId = e.target.closest("tr").dataset.id;
  const mainContent = document.getElementById("main-content");

  xhr = new XMLHttpRequest();
  xhr.open(
    "GET",
    `maintainance/device-malfunction-record-create/${deviceId}/`,
    true
  );
  xhr.onload = function () {
    if (this.status === 200) {
      const responseText = JSON.parse(this.responseText);
      if (responseText.message) {
        if (responseText.message == "fail") {
          alert("请先为该设备制定维护人！");
          return;
        }
      }
      content = responseText.content;
      mainContent.innerHTML = content;
    }
  };
  xhr.send();
}

function dispatchDeviceSubmit(e) {
  e.preventDefault();
  const deviceId = document.getElementById("device-id").innerText;
  data = new FormData(e.target);
  xhr = new XMLHttpRequest();
  xhr.open(
    "POST",
    `maintainance/device-malfunction-record-create/${deviceId}/`,
    true
  );
  xhr.onload = function () {
    if (this.status === 200) {
      const res = JSON.parse(this.responseText);
      if (res.message == "success") {
        alert("更新成功");
      } else {
        alert("更新失败！");
      }
      gotoLink("maintainance/device-list/0/")
    }
  };
  xhr.send(data);
}

function startMaintainance(e){
  const recordId = e.target.closest("tr").dataset.id
  xhr = new XMLHttpRequest();
  xhr.open(
    "PATCH",
    `maintainance/start-maintainance/${recordId}/`,
    true
  );
  xhr.onload = function () {
    if (this.status === 200) {
      const res = JSON.parse(this.responseText);
      if (res.message == "success") {
        gotoLink(`maintainance/maintainance-record-create/${recordId}/`)
      } else {
        alert("检修失败！");
      }
    }
  };
  xhr.send();
}

function maintainanceRecordCreate(e){
  let malfunctionRecordId
  if (e.target.closest("tr")){
    malfunctionRecordId = e.target.closest("tr").dataset.id
  }else {
    malfunctionRecordId = document.getElementById("malfunction_record_id").value
  }
  
  const mainContent = document.getElementById("main-content");

  xhr = new XMLHttpRequest();
  xhr.open(
    "GET",
    `maintainance/maintainance-record-create/${malfunctionRecordId}/`,
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

function maintainanceRecordCreateSubmit(e){
  e.preventDefault()
  const recordId = document.getElementById("malfunctionRecordId").value
  data = new FormData(e.target);
  xhr = new XMLHttpRequest();
  xhr.open(
    "POST",
    `maintainance/maintainance-record-create/${recordId}/`,
    true
  );
  xhr.onload = function () {
    if (this.status === 200) {
      const res = JSON.parse(this.responseText);
      if (res.message == "success") {
        alert("更新成功");
      } else {
        alert("更新失败！");
      }
      gotoLink(`maintainance/maintainance-record-list/${document.getElementById('malfunctionRecordId').value}/`)
    }
  };
  xhr.send(data);
}

function maintainanceRecordList(e){
  const malfunctionRecordId = e.target.closest("tr").dataset.id
  const mainContent = document.getElementById("main-content");

  xhr = new XMLHttpRequest();
  xhr.open(
    "GET",
    `maintainance/maintainance-record-list/${malfunctionRecordId}/`,
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

function checkMaintainanceRecordList(e){
  const malfunctionRecordId = e.target.closest("tr").dataset.id
  const mainContent = document.getElementById("main-content");
  const back_url = encodeURIComponent(document.getElementById("back-url").value)

  xhr = new XMLHttpRequest();
  xhr.open(
    "GET",
    `maintainance/maintainance-record-list/${malfunctionRecordId}/?back_url=${back_url}`,
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

function searchMalfunctionRecord(e){
  const deviceId = document.querySelector("#device-id").value;
  const equipmentName = document.querySelector("#equipment-name").value;
  const beginDate = document.getElementById("begin-date").value;
  const endDate = document.getElementById("end-date").value;
  const maintainerId = document.getElementById("maintainer-id").value;
  const mainContent = document.getElementById("main-content");

  xhr = new XMLHttpRequest();
  xhr.open(
    "GET",
    `maintainance/malfunction-record-query-list/?device_id=${deviceId}&equipment_name=${equipmentName}&begin_date=${beginDate}&end_date=${endDate}&maintainer_id=${maintainerId}&state=${document.getElementById('state').value}`,
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
