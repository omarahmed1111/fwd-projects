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
        
        listItem.innerHTML = `<a href="#${section.id}">${sectionName}</a>`;
        listFragment.appendChild(listItem);
    });

    navBarList.appendChild(listFragment);
}

function isInViewport(element) {
    const rect = element.getBoundingClientRect();
    return (
        rect.top >= -300 && rect.top <=300
    );
}

function removeAllHighlightedSections(){
    sections.forEach((section) => {
        section.classList.remove('your-active-class');
    });
}

function highlightActiveSection(){
    removeAllHighlightedSections();

    sections.forEach((section) => {
        if(isInViewport(section))
            section.classList.add('your-active-class');
    });
}


/**
 * End Helper Functions
 * Begin Main Functions
 * 
*/


// build the nav
buildNavBar();

// Add class 'active' to section when near top of viewport
let scrolling = false;

window.onscroll = () => {
    scrolling = true;
};

setInterval(() => {
    if (scrolling) {
        scrolling = false;
        highlightActiveSection();
    }

},100);

// Scroll to anchor ID using scrollTO event


/**
 * End Main Functions
 * Begin Events
 * 
*/

// Build menu 

// Scroll to section on link click

// Set sections as active


