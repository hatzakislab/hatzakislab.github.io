import { softwares } from "../data/softwares.js";

const softwaresContainer = document.querySelector('#software--container')

const logo = document.querySelector('#logo')
logo.style.opacity = '1'


softwares.forEach(soft => {

    softwaresContainer.insertAdjacentHTML('beforeend',
        `<div class="software--card">
        <img src="../images/software/${soft.img}" alt="kostas">
            <p class="title">${soft.title}</p>
            <p class="text">${soft.text}
            </p>
        </div>`
    )

})


