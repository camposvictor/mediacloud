const PROMPT_HTML = `
<div class="drop-zone__prompt flex flex-col items-center text-gray-500">
  <svg xmlns="http://www.w3.org/2000/svg" width="48" height="48" viewBox="0 0 24 24" fill="none"
    stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"
    class="lucide lucide-cloud-upload">
    <path d="M12 13v8" />
    <path d="M4 14.899A7 7 0 1 1 15.71 8h1.79a4.5 4.5 0 0 1 2.5 8.242" />
    <path d="m8 17 4-4 4 4" />
  </svg>
  <span class="text-center">
    Solte o arquivo aqui ou <button type="button" class="btn btn-link px-1">Escolher arquivo</button>
  </span>
</div>`;

document.addEventListener('DOMContentLoaded', () => {
  initializeDropZones();
});

function initializeDropZones() {
  document.querySelectorAll(".drop-zone__input").forEach(fileInput => {
    const dropZone = fileInput.closest(".drop-zone");
    const uploadButton = document.querySelector(".btn-upload");

    setUpEventListeners(fileInput, dropZone, uploadButton);
  });
}

function setUpEventListeners(fileInput, dropZone, uploadButton) {
  dropZone.addEventListener("click", () => fileInput.click());
  fileInput.addEventListener("change", () => handleFileChange(fileInput, dropZone, uploadButton));
  dropZone.addEventListener("dragover", event => handleDragOver(event, dropZone));
  dropZone.addEventListener("dragleave", () => handleDragLeave(dropZone));
  dropZone.addEventListener("drop", event => handleFileDrop(event, fileInput, dropZone, uploadButton));
}

function handleFileChange(fileInput, dropZone, uploadButton) {
  if (fileInput.files.length) {
    updateFileName(dropZone, fileInput.files[0]);
    enableUploadButton(uploadButton);
  } else {
    disableUploadButton(uploadButton);
    restoreDropZonePrompt(dropZone);
  }
}

function handleDragOver(event, dropZone) {
  event.preventDefault();
  dropZone.classList.add("border-indigo-600");
}

function handleDragLeave(dropZone) {
  dropZone.classList.remove("border-indigo-600");
}

function handleFileDrop(event, fileInput, dropZone, uploadButton) {
  event.preventDefault();
  if (event.dataTransfer.files.length) {
    fileInput.files = event.dataTransfer.files;
    updateFileName(dropZone, event.dataTransfer.files[0]);
    enableUploadButton(uploadButton);
  }
  dropZone.classList.remove("border-indigo-600");
}

function updateFileName(dropZone, file) {
  removeElement(dropZone, ".drop-zone__prompt");
  const fileNameElement = getOrCreateFileNameElement(dropZone);
  fileNameElement.textContent = file.name;
}

function getOrCreateFileNameElement(dropZone) {
  let fileNameElement = dropZone.querySelector(".drop-zone__filename");
  if (!fileNameElement) {
    fileNameElement = document.createElement("div");
    fileNameElement.classList.add("drop-zone__filename");
    dropZone.appendChild(fileNameElement);
  }
  return fileNameElement;
}

function restoreDropZonePrompt(dropZone) {
  removeElement(dropZone, ".drop-zone__filename");
  if (!dropZone.querySelector(".drop-zone__prompt")) {
    dropZone.insertAdjacentHTML('beforeend', PROMPT_HTML);
  }
}

function removeElement(container, selector) {
  const element = container.querySelector(selector);
  if (element) element.remove();
}

function enableUploadButton(button) {
  button.disabled = false;
}

function disableUploadButton(button) {
  button.disabled = true;
}

function openModal() {
  document.getElementById("my_modal_1").showModal();
}