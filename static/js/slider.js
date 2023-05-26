const slides = document.querySelectorAll('.slide');

let current = 0;
let next = 2;
let prev, center;


function toggleClass(element, oldClass, newClass) {
    element.classList.add(newClass);
    element.classList.remove(oldClass);
}

function slideFrames() {
    if ( current == 0 ) {
        prev = 4;
    } else {
        prev = current - 1;
    }

    if ( current == 4 ) {
        center = 0;
    } else {
        center = current + 1
    }

    if ( next == 4 ) {
        next = 0;
    } else {
        next = next + 1;
    }

    slides.forEach(slide => {
        const id = parseInt(slide.getAttribute('data-id'));
        if ( current == id ) {
            toggleClass(slide, 'left', 'prev');
        } else if ( prev == id ) {
            toggleClass(slide, 'prev', 'next');
        } else if ( next == id ) {
            toggleClass(slide, 'next', 'right');
        } else if ( center == id ) {
            toggleClass(slide, 'center', 'left');
        } else {
            toggleClass(slide, 'right', 'center');
        }
    })
    
    if ( current == 4 ) {
        current = 0;
    } else {
        current++;
    }
}


setInterval( () => {
    slideFrames();
}, 5000);
