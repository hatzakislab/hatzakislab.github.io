import { fundings } from "../data/fundings.js"


const fundingsContainer = document.querySelector('#fundings--container')




fundings.forEach(fund => {

    fundingsContainer.insertAdjacentHTML('beforeend',
        `  <div class="funding">
                <img  src="../images/fundings/${fund.img}" alt="Fund Image">
            </div>`

    )
})



