import { members } from '../data/members.js'

const logo = document.querySelector('#logo')
logo.style.opacity = '1'



const membersContainer = document.querySelector('#members--container')








members.forEach(member => {


    

    let memberMedia = `
    <ul  class="member--media">
    ${member?.linkedin 
        ?  `<li><a href="http://www.linkedin.com/in/${ member.linkedin }" target="_blank"><i
        class="fa fa-linkedin"></i></a></li>` : ``
    }
    ${member?.email 
        ? `<li><a href="mailto:${ member.email }"><i class="fa fa-envelope-square"></i></a></li>` : ``
    }
    ${member?.twitter
        ? `<li><a href="http://twitter.com/${ member.twitter }" target="_blank"><i
        class="fa fa-twitter"></i></a></li>` : ''
    }
    ${member?.facebook
        ?  `<li><a href="http://www.facebook.com/${ member.facebook }" target="_blank"><i
    class="fa fa-facebook"></i></a></li> ` : ''
    }
    ${member?.orcid
     ?  `<li><a href="http://www.orcid.org/${ member.orcid }" target="_blank"><i
     class="ai ai-orcid"></i></a></li>` : ''
    }
    ${member?.github
        ?  `<li><a href="http://github.com/${ member.github }" target="_blank"><i
        class="fa fa-github"></i></a></li>` : ''
    }
    ${member?.website
        ? `<li><a href="http://${ member.website }" target="_blank"><i
        class="fa fa-home"></i></a></li>` : ''
    }
    </ul>
    `

    membersContainer.insertAdjacentHTML('beforeend',
            `<div class="member--card">
                <div class="image--media--container">
                     ${ memberMedia.length > 90 ? memberMedia : ''}
                    <img class="member--pic" src="../images/team/${member.img}" alt="">
                </div>
                <p class="member--name">${member.name}</p>
                <p class="member--desc">${member.desc}</p>
            </div>`
    )
    
});


const membersMedia = document.querySelectorAll('.image--media--container');




membersMedia.forEach(media => {

    // console.log(media.children[0]);

    
    
    media.addEventListener('mouseover', ()=>{
         media.children[0].style['z-index'] = '4'
         media.children[1].style['opacity'] = '0.3'
    })


    media.addEventListener('mouseout', ()=>{
        media.children[0].style['z-index'] = '0'
        media.children[1].style['opacity'] = '1'
   })
    
  
        
    })




