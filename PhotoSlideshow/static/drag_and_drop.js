
$(document).ready(function(){
    // File type validation
       $("#fileInput").change(function(){
           var fileLength = this.files.length;
           var match= ["image/jpeg","image/png","image/jpg","image/gif"];
           var i;
           for(i = 0; i < fileLength; i++){ 
               var file = this.files[i];
               var imagefile = file.type;
               if(!((imagefile==match[0]) || (imagefile==match[1]) || (imagefile==match[2]) || (imagefile==match[3]))){
                   alert('Please select a valid image file (JPEG/JPG/PNG/GIF).');
                   $("#fileInput").val('');
                   return false;
               }
           }
       });
   });




//----------------------------------------------------
const gallery = document.getElementById('gallery');
const imageList = document.getElementById('image-list');
const selected = document.getElementById('selected');

function handleFiles(files) {    
    for (const file of files) {
        function onButtonClick() {
            const temp_img = document.createElement('img');
            temp_img.src = URL.createObjectURL(file);
            selected.appendChild(temp_img);
        }
    
        if (!file.type.startsWith('image/')) continue;

        const img = document.createElement('img');
        img.src = URL.createObjectURL(file);
        gallery.appendChild(img);
        img.addEventListener('click', onButtonClick);
    }
}

const dropArea = document.getElementById('drop-area');

['dragenter', 'dragover', 'dragleave', 'drop'].forEach(eventName => {
    dropArea.addEventListener(eventName, preventDefaults, false);
});

function preventDefaults(e) {
    e.preventDefault();
    e.stopPropagation();
}

['dragenter', 'dragover'].forEach(eventName => {
    dropArea.addEventListener(eventName, highlight, false);
});

['dragleave', 'drop'].forEach(eventName => {
    dropArea.addEventListener(eventName, unhighlight, false);
});

function highlight(e) {
    dropArea.classList.add('highlight');
}

function unhighlight(e) {
    dropArea.classList.remove('highlight');
}

dropArea.addEventListener('drop', handleDrop, false);

function handleDrop(e) {
    const dt = e.dataTransfer;
    const files = dt.files;
    handleFiles(files);
}

function playAudio() {
    var audioSelect = document.getElementById("audioSelect");
    var audioPlayer = document.getElementById("audioPlayer");
    var selectedAudio = audioSelect.value;

    audioPlayer.src = selectedAudio;
    audioPlayer.play();
}


const selecetdImages = document.querySelectorAll('#selected img');

function setResolution() {
    var resolutionSelect = document.getElementById("resolution_select");
    var selectedResolution = resolutionSelect.value;
    var selectedDiv = document.querySelectorAll("#selected img");
    for(var file of selectedDiv) {
        file.style.width = selectedResolution.split(" ")[0];
        file.style.height = selectedResolution.split(" ")[1];
    }
}

// var i = 0;
// const show_area = document.getElementById('slideshow');
// function slideshow() {
//     for(file in selectedImages){
//         show_area.appendChild(file);
//     }
// }   

