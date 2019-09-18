window.addEventListener("load", function (event) {
    let images = document.querySelectorAll("[data-original]");
    let lazy = lazyload(images, {
        "src": "data-original",
    });
});