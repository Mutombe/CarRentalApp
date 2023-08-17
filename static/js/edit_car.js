
    function previewCarPhoto(event) { 
        var preview = document.getElementById('car-photo-preview'); 
        var file = event.target.files[0]; 
        var reader = new FileReader(); 
        reader.onload = function() { 
            preview.src = reader.result; 
            preview.style.display ='inline'; 
        } 
        reader.readAsDataURL(file); 

        var inputField = event.target;
        inputField.style.width = "calc(100% - " + (preview.offsetWidth + 10) + "px)";
    } 
