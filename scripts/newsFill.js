import { news } from "../data/news.js"


const newsContainer = document.querySelector('#news--container')

const logo = document.querySelector('#logo')
logo.style.opacity = '1'





news.forEach( newsUnit => {

    newsContainer.insertAdjacentHTML('beforeend',
    `<div class="news--card">
        <div class="info">
        <p class="title">${newsUnit.title}</p>
        <p class="date">${newsUnit.date}</p>
        <p class="text">${newsUnit.text}</p>
        ${newsUnit?.link ? `<a href="${newsUnit.link}" target="_blank">See article</a>` : '' }
        </div>
    ${newsUnit?.image ?
    `<div class="img--div">
    
        <img src="../images/news/${newsUnit.image}" alt="News image">
    </div>` : ''
    }

</div>`

    )
})



