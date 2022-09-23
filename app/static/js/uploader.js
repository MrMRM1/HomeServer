// Get a reference to the 3 buttons
var upload_btn = document.getElementById("upload_btn");
var loading_btn = document.getElementById("loading_btn");
var cancel_btn = document.getElementById("cancel_btn");

// Get a reference to the alert wrapper
var alert_wrapper = document.getElementById("alert_wrapper");

// Get a reference to the file input element & input label 
var input = document.getElementById("file_input");
var file_input_label = document.getElementById("file_input_label");
var file_input_size = document.getElementById("file_input_size");
let number_file_uploaded = 0;
let file_index = 0;
let number_files = 0;
let input_url = "/send";
// 
let file_boxes = document.getElementById("file_boxes");
let files_canceled = [];
// Function to show alerts
function show_alert(message, alert) {

  alert_wrapper.innerHTML = `
    <div id="alert" class="alert alert-${alert} alert-dismissible fade show" role="alert">
      <span>${message}</span>
      
      </button>
    </div>
  `
    setTimeout(function () {
        alert_wrapper.innerHTML = '';
    }, 10000);

}

function checked(){
  if (input.files.length != 0){
     file_index += 1;
    if (number_files != number_file_uploaded){
      file_input_label.innerText = number_files_upload();
      upload_multiple(input_url);
    }
    else if ((number_file_uploaded == 0) && (number_files == number_file_uploaded)){
      show_alert(`Upload cancelled`, "primary");
      reset();
    }
    else if (number_files == number_file_uploaded) {
      show_alert(`File uploaded ` + number_files_upload(), "success");
      reset();
    }
  }
}
function cancel_push(index){
  if ((input.files.length != 0) && (!files_canceled.includes(index))){
    files_canceled.push(index)
    number_files = input.files.length - files_canceled.length
    file_input_label.innerText = number_files_upload();
    set_size()
  }
}

function remove_box_file(index){
  document.getElementById(`file${index}`).remove()
  if (input.files.length != 0){
    cancel_push(index)
  }
}

function generate_box_file(index){
  let tag = `<div id="file${index}" class="col-md-6 col-11 ms-auto me-auto mt-2 border rounded-3">
  <div class="m-3 mt-4 float-start">
      <div id="file${index}_loading" class="spinner-border text-primary" role="status">
          <span class="visually-hidden">Loading...</span>
      </div>
      <div>
          <img class="d-none" id="file${index}_done" src="static/icon/done.svg" />
      </div>
  </div>
  <button onclick="remove_box_file(${index})" id="file${index}_close" type="button" class="btn-close float-end m-3 mt-4" aria-label="Close"></button>
  <div class="mt-2 text-break">
      <p id="file${index}_name">${input.files[index].name}</p>
  </div>
  <div class="d-flex">
      <p id="file${index}_size">File Size : ${change_size_number(input.files[index].size)} |</p>
      <p class="ms-1" id="file${index}_progress_status">0% uploaded</p>
  </div>
  <div class="col-10 me-auto ms-auto">
      <div class="progress mb-2">
          <div id="file${index}_progress" class="progress-bar progress-bar-striped progress-bar-animated" role="progressbar" aria-valuenow="25" aria-valuemin="0" aria-valuemax="100"></div>
      </div>
  </div>
</div>`
file_boxes.innerHTML += tag
}

function create_box_file(){
  file_boxes.innerHTML = ''
  files_canceled = [];
  for (let i=0; i<input.files.length; i++){
    generate_box_file(i)
  }
}

function upload_multiple() {
  if (!input.value) {

    show_alert("No file selected", "warning")

    return;

  }
  if ((number_file_uploaded == 0) && (files_canceled.length == 0)){
    number_files = input.files.length;
    create_box_file()
  }
  upload(input_url, file_index)
}

// Function to upload file
function upload(url, files_number) {

  // Reject if the file input is empty & throw alert
  if (!input.value) {

    show_alert("No file selected", "warning")

    return;

  }
  // Get a reference to the progress bar, wrapper & status label
  var progress = document.getElementById(`file${files_number}_progress`);
  var progress_status = document.getElementById(`file${files_number}_progress_status`);
  var loading_file = document.getElementById(`file${files_number}_loading`);
  var done_file = document.getElementById(`file${files_number}_done`);

  // Create a new FormData instance
  var data = new FormData();

  // Create a XMLHTTPRequest instance
  var request = new XMLHttpRequest();

  // Set the response type
  request.responseType = "json";

  // Clear any existing alerts
  alert_wrapper.innerHTML = "";

  // Disable the input during upload
  input.disabled = true;

  // Hide the upload button
  upload_btn.classList.add("d-none");

  // Show the loading button
  loading_btn.classList.remove("d-none");

  // Show the cancel button
  cancel_btn.classList.remove("d-none");

  // Get a reference to the file
  var file = input.files[files_number];

  if (!files_canceled.includes(files_number)){

    // Get a reference to the filesize & set a cookie
    var filesize = file.size;
    document.cookie = `filesize=${filesize}`;

    // Append the file to the FormData instance
    data.append("file", file);

    // request progress handler
    request.upload.addEventListener("progress", function (e) {

      // Get the loaded amount and total filesize (bytes)
      var loaded = e.loaded;
      var total = e.total

      // Calculate percent uploaded
      
      var percent_complete = (loaded / total) * 100;

      // Update the progress text and progress bar
      progress.setAttribute("style", `width: ${Math.floor(percent_complete)}%`);
      progress_status.innerText = `${Math.floor(percent_complete)}% (` + change_size_number(loaded) + `) uploaded`;

    })

    // request load handler (transfer complete)
    request.addEventListener("load", function (e) {

      if (request.status == 200) {
        loading_file.classList.add('d-none');
        done_file.classList.remove('d-none')
        number_file_uploaded += 1 ;
        checked()
      }
      else {

        show_alert(`Error uploading file`, "danger");

      }

    });

    // request error handler
    request.addEventListener("error", function (e) {

      reset();

      show_alert(`Error uploading file`, "warning");

    });

    // Open and send the request
    request.open("post", url);
    request.send(data);

    cancel_btn.addEventListener("click", function () {
      request.abort();
      reset();
      file_boxes.innerHTML = ''
      show_alert(`Upload cancelled`, "primary");

    })
    document.getElementById(`file${files_number}_close`).addEventListener("click", function () {
      request.abort();
      checked()
    })

  }
  else{
    checked()
  }

}

function change_size_number(n){
    var measure = "KB";
    var sizefile = n/1024;
    function conversion(d){
        return (d/1024);
    }
    if (sizefile >= 1000){
        sizefile = conversion(sizefile);
        measure = "MB";
    }
    if (sizefile >= 1000){
        sizefile = conversion(sizefile);
        measure = "GB";
    }

    return sizefile.toFixed(2) + measure;
}

function number_files_upload(){
  return  "(" + number_file_uploaded + "/" + number_files + ")" ;
}

// Function to update the input placeholder
function input_filename() {
  number_files = input.files.length;
  file_input_label.innerText = number_files_upload() ;
  set_size()
}

function set_size(){
  let sizes = 0 ;
  for (var i=0; i < input.files.length; i++){
    if (!files_canceled.includes(i)){
      sizes = sizes + input.files[i].size;
    }
    
  }
  file_input_size.innerText = change_size_number(sizes) ;
}

// Function to reset the page
function reset() {

  // Clear the input
  input.value = null;

  // Hide the cancel button
  cancel_btn.classList.add("d-none");

  // Reset the input element
  input.disabled = false;

  // Show the upload button
  upload_btn.classList.remove("d-none");

  // Hide the loading button
  loading_btn.classList.add("d-none");

  // Hide the progress bar
  files_canceled = [];
  file_index = 0;
  number_file_uploaded = 0;
  number_files = 0;
  file_input_label.innerText = "0";
  file_input_size.innerText = "";

}