const body = document.body;
const closePopupButton = document.querySelector('#close--popup--button');



const whatWeDoButton = document.querySelector('#what--we--do');
const ourHistoryButton = document.querySelector('#our--history');
const contactUsButton = document.querySelector('#contact--us');



const whatWeDoText = `The main objective of my group is to augment our understanding
    on the molecular mechanisms that underlie and control vital cellular functions.
    We approach this challenge by deciphering the dynamic interplay between the function and spatiotemporal
    localization of biomolecules (virus, dug nanocarrier, oligonucleotides or protein assemblies) and how this 
    correlate to cellular and organismal response.
    
    <br><br>
    
    We have therefore pioneered the development of novel new imaging technologies - 
    with an emphasis on single particle and live cell microscopy - that promises to shed 
    light on the interplays between the behavior (dynamics, function and localization) of 
    biomolecules and high throughput single particle screening methodologies to decipher oligonucleotide
    interactions with membranes. By tracking the spatiotemporal displacement
    and localization of one protein - or an assembly - in real time we revealed internalization pathways
    and cell fate of nanoparticles and viruses. Our functional and FRET studies at the fundamental limit 
    of individual catalytic cycle, on the other hand have helped deciphering protein structure and function
    dependence on temporal cell localization and the design of novel ligand biasing aberrant biological function.
    
    <br><br>
    
    Recognizing that 4D imaging generates terabytes of data sets,
    that are prohibitively hard to be quantitatively evaluated by 
    current semi-manual analysis, we have developed toolboxes and softwares
    based on machine learning to rapidly, reliably and free of human cognitive biases, 
    analyze the wealth of novel microscopy data we, and others, produce. Our all-inclusive softwares
    for windows and macs, offer transition from raw data to quantitative analysis and data classification 
    with less than 5 clicks, accelerating the automatic analysis by ~6 orders of magnitude. These combined 
    methodologies bridge 4D imaging with sophisticate image analysis required for delving into the era of 4D
    cell and tissue imaging.`;


const ourHistoryText = `Embarking on a journey through time, our history is woven with innovation and perseverance.
 From humble beginnings to the present, we've charted a course marked by milestones in science and technology.
 
 <br><br>
 
 Founded with a passion to unravel the world's mysteries, our early years set the stage. 
 As we navigated research and discovery, our commitment to excellence remained unwavering.
 
 <br><br>
 
 Our history is linked to breakthroughs in scientific methodologies. 
 Pioneering novel approaches became our hallmark, leading to cutting-edge technologies that redefine how we 
 perceive and interact with science.<br><br>Chapters unfold with a spotlight on comprehensive imaging technologies.
Embracing single-particle and live cell microscopy, we unraveled dynamic biomolecule interplay. 
High-throughput screening methodologies allowed deciphering intricate interactions.

<br><br>

Recent chapters focus on real-time tracking, unveiling internalization pathways and cellular destinies. 
Functional and FRET studies reached fundamental limits, deciphering protein structure and function dependence.

<br><br>

Our history takes a transformative leap into 4D imaging, pioneering machine learning toolboxes. 
These advancements facilitate rapid, bias-free analysis of vast microscopy datasets, accelerating 
understanding.

<br><br>

In essence, our history mirrors a relentless pursuit of knowledge and innovation. 
Each chapter represents a testament to our commitment to advancing scientific understanding. The future awaits, 
and we continue to inscribe new chapters, driven by the spirit that defines our journey.`;

    


whatWeDoButton.addEventListener('click', () => createPopUp('What we do.',whatWeDoText))
ourHistoryButton.addEventListener('click',() => createPopUp('Our history.',ourHistoryText))












function createPopUp(title, text) {

    
    body.insertAdjacentHTML('afterbegin', `
        <div id="pop--up--info">
            <p>${title}</p>
            <i class="fa-solid fa-x" id="x"></i>
            <div class="blue--red">
            <div class="blue"></div>
            <div class="red"></div>
            </div>
            <article>${text}</article>
            <button id="close--popup--button">Close</button>
        </div>
    `);

    body.style.overflow = 'hidden';

    const popUpInfo = document.getElementById('pop--up--info');
    const popUpSiblings = body.children;

    popUpInfo.style.display = 'flex';

    for (let i = 0; i < popUpSiblings.length; i++) {
        const child = popUpSiblings[i];
        if (child !== popUpInfo) {
            child.classList.add('blur');
        }
    }



    const closePopupButton = document.querySelector('#close--popup--button');
    const x = document.querySelector('#x')


    closePopupButton.addEventListener('click', () => {
        const popUpInfo = document.getElementById('pop--up--info');
        popUpInfo.remove()


        body.style.overflow = ''; // Enable scrolling

        for (let i = 0; i < popUpSiblings.length; i++) {
            const child = popUpSiblings[i];
            if (child !== popUpInfo) {
                child.classList.remove('blur');
            }
        }
    });


    x.addEventListener('click', () => {
        const popUpInfo = document.getElementById('pop--up--info');
        popUpInfo.remove()


        body.style.overflow = ''; // Enable scrolling

        for (let i = 0; i < popUpSiblings.length; i++) {
            const child = popUpSiblings[i];
            if (child !== popUpInfo) {
                child.classList.remove('blur');
            }
        }
    });


    
    
}



