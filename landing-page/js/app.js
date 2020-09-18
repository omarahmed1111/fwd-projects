/**
 * 
 * Manipulating the DOM exercise.
 * Exercise programmatically builds navigation,
 * scrolls to anchors from navigation,
 * and highlights section in viewport upon scrolling.
 * 
 * Dependencies: None
 * 
 * JS Version: ES2015/ES6
 * 
 * JS Standard: ESlint
 * 
*/

/**
 * Define Global Variables
 * 
*/
const pageHeader = document.querySelector('.page__header');
const navBar = pageHeader.firstElementChild;
const navBarList = navBar.firstElementChild;

const main = document.querySelector('main');
const sections = main.querySelectorAll('section');



/**
 * End Global Variables
 * Start Helper Functions
 * 
*/


function buildNavBar(){

    const listFragment = document.createDocumentFragment();

    sections.forEach((section) => {
        const listItem = document.createElement('li');
        const sectionName = section.getAttribute('data-nav');
        
        listItem.textContent = sectionName;
        listFragment.appendChild(listItem);
    });

    navBarList.appendChild(listFragment);
}


/**
 * End Helper Functions
 * Begin Main Functions
 * 
*/

// build the nav
buildNavBar();

// Add class 'active' to section when near top of viewport


// Scroll to anchor ID using scrollTO event


/**
 * End Main Functions
 * Begin Events
 * 
*/

// Build menu 

// Scroll to section on link click

// Set sections as active


