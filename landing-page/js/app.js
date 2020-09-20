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
const navBarList = document.querySelector('#navbar__list');

const sections = document.querySelectorAll('section');



/**
 * End Global Variables
 * Start Helper Functions
 * 
*/
// Helper function to build dynamically the navbar from page sections.
function buildNavBar(){

    const listFragment = document.createDocumentFragment();

    // Loop through sections of the page and add a link in the navbar for navigating to it.
    sections.forEach((section) => {
        const listItem = document.createElement('li');
        const sectionName = section.getAttribute('data-nav');
        
        listItem.innerHTML = `<a href="#${section.id}">${sectionName}</a>`;
        listFragment.appendChild(listItem);
    });

    navBarList.appendChild(listFragment);
}

// Helper function to check whether the element is present in the current viewport.
function isInViewport(element) {
    const rect = element.getBoundingClientRect();
    return (
        rect.top >= -300 && rect.top <=300
    );
}

// Helper function to remove all highlighted section on the page.
function removeAllHighlightedSections(){
    sections.forEach((section) => {
        section.classList.remove('your-active-class');
    });
}

// Helper function to highlight only active sections.
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


/**
 * End Main Functions
 * Begin Events
 * 
*/

// Add class 'active' to section when near top of viewport
let scrolling = false;

window.onscroll = () => {
    scrolling = true;
};
// Delay the scrolling event to prevent overflow of memory.
setInterval(() => {
    if (scrolling) {
        scrolling = false;
        highlightActiveSection();
    }

},100);

