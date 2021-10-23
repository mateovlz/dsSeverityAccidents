/********* Menu Functionality ***********/

const menuButton = document.getElementById('menu');
const menuContainer = document.querySelector('.container-menu');
const menuCompleted = document.querySelector('.container-menu-completed');
const menuExit = document.querySelector('.menu-exit');

menuButton.addEventListener('click',()=>{
    menuContainer.style.visibility = "visible";
    menuContainer.style.transform = 'translateX(0)';
    menuCompleted.style.visibility = "visible";
    menuCompleted.style.transform = 'translateX(0)';

});


menuCompleted.addEventListener('click',()=>{
    menuContainer.style.visibility = 'hidden';
    menuContainer.style.transform = 'translateX(-100%)';
    menuCompleted.style.visibility = 'hidden';
    menuCompleted.style.transform = 'translateX(-80%)';

});

menuExit.addEventListener('click',()=>{
    menuContainer.style.visibility = 'hidden';
    menuContainer.style.transform = 'translateX(-100%)';
    menuCompleted.style.visibility = 'hidden';
    menuCompleted.style.transform = 'translateX(-80%)';

});
