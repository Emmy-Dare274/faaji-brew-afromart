document.addEventListener("DOMContentLoaded", function () {
    var scrollBtn = document.getElementById("scrollTopBtn");
    if (!scrollBtn) return;

    window.addEventListener("scroll", function () {
        scrollBtn.classList.toggle("show", window.scrollY > 400);
    });

    scrollBtn.addEventListener("click", function () {
        window.scrollTo({ top: 0, behavior: "smooth" });
    });
});