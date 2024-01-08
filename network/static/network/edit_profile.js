document.addEventListener("DOMContentLoaded", function(){

    uploadImageValidation();
    

    const aboutInput = document.getElementById("about-input");
    const characterCounter = document.getElementById("character-counter");
    characterCounter.style.display = 'none';

    aboutInput.addEventListener("input", function(){
        const maxLength = 225;
        const currentLength = aboutInput.value.length;
        const remaining = maxLength - currentLength;

        if (remaining < 50){
            characterCounter.style.color = "red";
        }
        else{
            characterCounter.style.color = "#666";
        }

        //Toggle visibility based on user input
        if (currentLength > 0){
            characterCounter.style.display = "block";
        }
        else{
            characterCounter.style.display = "none";
        }

        characterCounter.textContent = remaining + "characters remaining";
    });
});


function uploadImageValidation(){
    let fileInput = document.querySelector("form input[type=file]");
    let fileInputLabel = document.querySelector(".custom-image-label")

    fileInput.addEventListener("change", (event) => {
        let file = event.target.files[0];
        //convert the file size from bytes to megabytes, Computer measures file in bytes
        let fileSize = file.size/1024/1024;
        let fileType = file.type;
        let fileName = file.name;

        //check if file is an image
        //fileType.indexOf("image") === -1 checks if the index of "image" is -1, which means "image" was not found in the fileType string.
        if (typeof fileType == "undefined" || fileType.indexOf("image") === -1){
            document.getElementById("file-type-error").classList.remove("hidden");

            //clear file button value
            fileInput.value = null;

            //clear file button placeholder
            fileInputLabel.innerHTML = fileInputLabel.dataset.default;
        }
        else if(fileSize > 2){
            document.getElementById("file-size-error").classList.remove("hidden");

            //clear file button value
            fileInput.value = null;

            //clear file button placeholder
            fileInputLabel.innerHTML = fileInputLabel.dataset.default;
        }
        // Change file button placeholder to file name
        else{
            fileInputLabel.innerHTML = fileName;
        }
    });
}