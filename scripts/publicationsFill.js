import {publications} from '../data/publications.js'



const logo = document.querySelector('#logo')
logo.style.opacity = '1'




const publicationsContainer = document.querySelector('#publications--container')


publications.forEach(publication => {
    publicationsContainer.insertAdjacentHTML('beforeend',
    `
    <div class="publication--card">
    <p class="journal">${publication.journal}</p>
    <a href=${publication.link} target="_blank" class="publication--title">${publication.title}</a>
    <img src="${publication.img}" alt="Publication Image">
    <div class="rest--info">
      <p class="author">${publication.author}</p>
      <p class="pages">${publication.pages}</p>
      <p class="year">${publication.year}</p>
    </div>

  </div>
    `)
})
