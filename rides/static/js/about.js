const counterEls = document.querySelectorAll('.counter');

const observer = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
        if (entry.isIntersecting) {
            increamentCount(entry);
        }
    })
})

counterEls.forEach((counterEl) => {
    observer.observe(counterEl);
})

function increamentCount(element) {
    const number = parseInt(element.target.getAttribute("data-number"));
    let current = parseInt(element.target.textContent);
    const i = setInterval( () => {
        if ( current < number ) {
            element.target.textContent = current++;
        } else {
            clearInterval(i);
        }
    }, 0)
}