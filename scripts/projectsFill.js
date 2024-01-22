// import { projects } from '../data/projects.js'




// const projectsContainer = document.querySelector('#projects--container')

// const circleContainer = document.querySelector('.circle-container');


// console.log(circleContainer);

// projects.forEach(project => {

//     projectsContainer.insertAdjacentHTML('beforeend',

//         `
//     <div class="project--card" onclick="window.location.href='./projects_page/projects.html#${project.id}'">
//       <div  class="button">${project.description}</div>
//       <img src="./images/${project.image}" " alt="image">
//     </div>
//     `
//     )
// });



// projects.forEach(project => {
//   circleContainer.insertAdjacentHTML('beforeend',
//       `
//       <div class="project" onclick="window.location.href='/projects_page/projects.html#${project.id}'">
//           <div class="project-wrapper">
//               <p>${project.description}</p>
//               <img src="../images/${project.image}" alt="Project Image">
//           </div>
//       </div>
//       ` 
//   );
// });



// const numberOfProjects = projects.length; // Change this number based on your projects



// const projectsItems = document.querySelectorAll('.project');
// const angle = 360 / projects.length;

// projectsItems.forEach((proj, index) => {
//   const rotateAngle = angle * index;
//   proj.style.transform = `rotate(${rotateAngle}deg) translate(25rem) rotate(-${rotateAngle}deg)`;

// });







const logo = document.querySelector('#logo')
logo.style.opacity = '1'