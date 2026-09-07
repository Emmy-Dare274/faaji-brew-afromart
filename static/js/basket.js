document.addEventListener("DOMContentLoaded", function () {
    var dropdown = document.getElementById("miniCartDropdown");
    if (!dropdown) return;

    document.body.addEventListener("submit", function (event) {
        var form = event.target;
        if (!form.classList.contains("add-to-basket-form")) return;

        event.preventDefault();
        fetch(form.action, {
            method: "POST",
            headers: { "X-Requested-With": "XMLHttpRequest" },
            body: new FormData(form),
        })
            .then(function (response) { return response.json(); })
            .then(function (data) {
                if (!data.success) {
                    showToast(data.error, "error");
                    return;
                }
                populateMiniCart(data);
                dropdown.classList.add("show");
                document.getElementById("navBasketTotal").textContent = data.basket_total;
                document.getElementById("navBasketCount").textContent = data.basket_item_count;
            })
            .catch(function () {
                form.submit();
            });
    });

    function populateMiniCart(data) {
        document.getElementById("miniCartAddedMsg").textContent = "Added " + data.added_product_name + " to your basket";
        document.getElementById("miniCartCountLabel").textContent = "Your Basket (" + data.basket_item_count + ")";

        var itemsHtml = data.items.map(function (item) {
            return '<div class="mini-cart-item">' +
                '<img src="' + item.product_image + '" alt="' + item.product_name + '">' +
                '<div><p class="fw-semibold mb-0 small">' + item.product_name + '</p>' +
                (item.variant ? '<p class="text-muted small mb-0">' + item.variant + '</p>' : '') +
                '<p class="text-muted small mb-0">Qty: ' + item.quantity + ' &middot; $' + item.line_total + '</p></div>' +
                '</div>';
        }).join('');
        document.getElementById("miniCartItems").innerHTML = itemsHtml;
        document.getElementById("miniCartTotal").textContent = "$" + data.basket_total;

        var noteEl = document.getElementById("miniCartDeliveryNote");
        if (data.qualifies_for_free_delivery) {
            noteEl.className = "free-delivery-banner qualified";
            noteEl.textContent = "You've unlocked free delivery!";
        } else {
            noteEl.className = "free-delivery-banner";
            noteEl.textContent = "Spend $" + data.amount_to_free_delivery + " more to get free delivery!";
        }
    }

    dropdown.querySelector(".mini-cart-close").addEventListener("click", function () {
        dropdown.classList.remove("show");
    });

    document.addEventListener("click", function (event) {
        if (!dropdown.contains(event.target) && !event.target.closest(".add-to-basket-form")) {
            dropdown.classList.remove("show");
        }
    });
});