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

function showToast(message, tone) {
    var container = document.querySelector(".toast-container");
    if (!container) return;

    var bg = tone === "error" ? "bg-danger" : tone === "info" ? "bg-info" : "bg-success";
    var toastEl = document.createElement("div");
    toastEl.className = "toast align-items-center text-white border-0 " + bg;
    toastEl.setAttribute("role", "alert");
    toastEl.innerHTML =
        '<div class="d-flex">' +
        '<div class="toast-body">' + message + '</div>' +
        '<button type="button" class="btn-close btn-close-white me-2 m-auto" data-bs-dismiss="toast"></button>' +
        '</div>';

    container.appendChild(toastEl);
    new bootstrap.Toast(toastEl, { delay: 4000 }).show();
}