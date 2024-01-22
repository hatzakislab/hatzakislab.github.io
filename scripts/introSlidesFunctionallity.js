document.querySelector('video').playbackRate = .8;

let descriptionHolder = document.querySelector('#videos--descriptions')

let purple = document.querySelector('#purple');
let annete = document.querySelector('#annete');
let group = document.querySelector('#group');

let slides = [purple, annete, group];

let dots = document.querySelectorAll('.dot');

let rightArrow = document.querySelector("#right--arrow");
let leftArrow = document.querySelector("#left--arrow");

let currentSlide = 0;

let descriptions = ['Particles movement observation.',"Some other thing that I don't remember.",'Our group photo.']


const showSlide = (slide) => {

  slides.forEach(sl => sl.classList.add('disabled'))
  slides.forEach(sl => sl.classList.remove('active'))


  slides[slide].classList.remove('disabled');
  slides[slide].classList.add('active');

  descriptionHolder.innerHTML = descriptions[slide]


};


showSlide(0)

const handleDotClick = (index) => {
  dots.forEach(dot => dot.classList.remove('selected'))
  dots[index].classList.add('selected')
  showSlide(index)

};

const handleLeftArrowClick = () => {
  if (currentSlide > 0) {
    currentSlide--;
  } else {
    currentSlide = 2;
  }
  showSlide(currentSlide);
  dots.forEach(dot => dot.classList.remove('selected'))
  dots[currentSlide].classList.add('selected')
};

const handleRightArrowClick = () => {
  if (currentSlide < 2) {
    currentSlide++;
  } else {
    currentSlide = 0;
  }
  showSlide(currentSlide);
  dots.forEach(dot => dot.classList.remove('selected'))
  dots[currentSlide].classList.add('selected')
};

dots.forEach((dot, index) => {
  dot.addEventListener("click", () => {
  
    handleDotClick(index);
  });
});

leftArrow.addEventListener("click", handleLeftArrowClick);
rightArrow.addEventListener("click", handleRightArrowClick);



setInterval(() => {
  handleRightArrowClick();
}, 10000);