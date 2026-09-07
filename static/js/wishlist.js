document.addEventListener("DOMContentLoaded", function () {
    document.body.addEventListener("submit", function (event) {
        var form = event.target;
        if (!form.classList.contains("wishlist-form")) return;

        event.preventDefault();
        fetch(form.action, {
            method: "POST",
            headers: { "X-Requested-With": "XMLHttpRequest" },
            body: new FormData(form),
        })
            .then(function (response) {
                if (!response.ok && response.status !== 401) throw new Error("Request failed");
                return response.json();
            })
            .then(function (data) {
                if (data.login_required) {
                    showToast("Please log in to save items to your favourites.", "info");
                    setTimeout(function () {
                        window.location.href = data.login_url;
                    }, 1400);
                    return;
                }

                var button = form.querySelector(".wishlist-heart-btn");
                button.classList.toggle("active", data.wishlisted);
                button.querySelector("i").className = data.wishlisted ? "bi bi-heart-fill" : "bi bi-heart";

                var countEl = document.getElementById("wishlistCount");
                if (countEl) countEl.textContent = data.count;

                var onWishlistPage = document.getElementById("wishlistGrid");
                if (!data.wishlisted && onWishlistPage) {
                    var card = form.closest("[data-product-slug]");
                    if (card) card.remove();
                }
            })
            .catch(function () {
                form.submit();
            });
    });
});

function showToast(message, tone) {
    var container = document.querySelector(".toast-container");
    if (!container) return;

    var bg = tone === "error" ? "bg-danger" : "bg-info";
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