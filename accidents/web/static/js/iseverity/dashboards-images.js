/********* Popup Functionality Images *********/
// Created constants of components of html to create popup image 
const selectedImage = document.getElementById('selected-image');
const popup = document.getElementById('popup-image');
const popupTitleImg = document.getElementById('popup-title-img');
var imageselected = '';
// Add evenListeners of clicks in every image to popup 
var images = document.getElementsByClassName('dashboard-image');
for(let image of images){

    image.addEventListener('click',()=>{
        popup.style.transform = 'translateY(0)';
        selectedImage.src = image.src;
        popupTitleImg.innerHTML  = image.alt;
    });
}

// Deleted popup from the view
popup.addEventListener('click',()=>{
    popup.style.transform = 'translateY(-100%)';
});
