const header = document.querySelector('#header')
const headerUl = document.querySelector('#header ul')
const headerLi = document.querySelectorAll('#header li')
const menuBar = document.querySelector('#menu--bar')
const body = document.querySelector('body')
const logoBarWrapper = document.querySelector('#wrapper')



let menuIsOpen = false;




const toggleMenu = () => {


    if(!menuIsOpen){

         
    body.style.overflow = 'hidden'

    headerUl.style.display = 'flex'
    headerUl.style['flex-direction']= 'column'
    headerUl.style.height = '50vh'
    headerUl.style.width = '100%';
    headerUl.style.margin = 0;


    header.style.padding = 0;
    header.style.height = '65vh'
    header.style['z-index'] = '2'


    headerLi.forEach(li => {
        li.style['font-family'] = "Montserrat, sans-serif";
        li.style['letter-spacing'] = "3px";
        li.style['margin-top'] = "13px";
        li.style['font-size'] = "1.1rem";
    })

    menuIsOpen = true;

    }else{
        headerUl.style.display = 'none'
        headerUl.style.height = '3rem'
        header.style.height = '3rem'


        menuIsOpen = false;
   

    }
}







if (window.innerWidth < 600) {

    for(let i=0;i<headerLi.length; i++){
        headerLi[i].addEventListener('click',toggleMenu)
     }

    
    menuBar.addEventListener('click', toggleMenu)

}


