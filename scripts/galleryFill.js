import { pictures } from "../data/gallery.js"

const galleryContainer = document.querySelector('#gallery--container')
const logo = document.querySelector('#logo')
logo.style.opacity = '1'



pictures.forEach(pic => {



    galleryContainer.insertAdjacentHTML('beforeend',
    `

    <img class="" src="../images/gallery/${pic.img}" alt="${pic.title}">
    `
    )
})