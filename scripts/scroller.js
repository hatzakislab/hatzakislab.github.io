
const observer = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
        if (entry.isIntersecting) {
            entry.target.classList.add('show');
        }
    });
}, {
    rootMargin: '400px' // Adjust this value as needed
});

const hiddenElements = document.querySelectorAll('.hidden');
hiddenElements.forEach(el => observer.observe(el));





const learnMoreButton = document.querySelector('#learn--more')

function scrollToMission() {
    const targetElement = document.getElementById('mission');
    if (targetElement) {
        const offset = 139; // Convert 5rem to pixels, assuming 1rem = 16px
        const bodyRect = document.body.getBoundingClientRect().top;
        const elementRect = targetElement.getBoundingClientRect().top;
        const elementPosition = elementRect - bodyRect;
        const offsetPosition = elementPosition - offset;

        window.scrollTo({
            top: offsetPosition,
            behavior: 'smooth'
        });
    }
}


learnMoreButton.addEventListener('click', scrollToMission)