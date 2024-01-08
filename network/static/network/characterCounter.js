document.addEventListener("DOMContentLoaded", function(){

    const aboutInput = document.getElementById("about-input");
    const characterCounter = document.getElementById("character-counter");
    characterCounter.style.display = 'none';

    aboutInput.addEventListener("input", function(){
        const maxLength = 1000;
        const currentLength = aboutInput.value.length;
        const remaining = maxLength - currentLength;

        if (remaining < 100){
            characterCounter.style.color = "red";
        }
        else{
            characterCounter.style.color = "blue";
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