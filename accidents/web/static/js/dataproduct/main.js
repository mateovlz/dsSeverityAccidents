/********* Popup Functionality Images *********/
// Created constants of components of html to create popup image 
const selectedImage = document.getElementById('selected-img');
const popup = document.getElementById('popup');
var imageselected = '';
// Add evenListeners of clicks in every image to popup 
var images = document.getElementsByClassName('images');
for(let image of images){

    image.addEventListener('click',()=>{
        popup.style.transform = 'translateY(0)';
        selectedImage.src = image.src;

    });
}
// Deleted popup from the view
popup.addEventListener('click',()=>{
    popup.style.transform = 'translateY(-100%)';
});

