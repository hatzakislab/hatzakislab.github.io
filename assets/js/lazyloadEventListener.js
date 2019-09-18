window.addEventListener("load", function (event) {
    let images = document.querySelectorAll("[data-original]");
    let lazy = lazyload(images, {
        "src": "data-original",
    });

    for (var i = 0; i < images.length; i++) {
        images[i].classList.remove('lazy')
    }

});