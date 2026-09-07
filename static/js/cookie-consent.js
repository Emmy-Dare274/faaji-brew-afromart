document.addEventListener("DOMContentLoaded", function () {
    var STORAGE_KEY = "afromart_cookie_consent";
    var banner = document.getElementById("cookieConsentBanner");
    var acceptAllBtn = document.getElementById("cookieAcceptAllBtn");
    var essentialOnlyBtn = document.getElementById("cookieEssentialOnlyBtn");
    var manageBtn = document.getElementById("manageCookiesBtn");
    if (!banner) return;

    function showBanner() {
        banner.hidden = false;
    }

    function hideBanner() {
        banner.hidden = true;
    }

    function setConsent(value) {
        localStorage.setItem(STORAGE_KEY, value);
        hideBanner();

        // Nothing non-essential is loaded on the Site for now, so this is a
        // no-op for now.
        if (value === "all") {
            document.dispatchEvent(new CustomEvent("cookieConsentGranted"));
        }
    }

    if (!localStorage.getItem(STORAGE_KEY)) {
        showBanner();
    }

    acceptAllBtn.addEventListener("click", function () {
        setConsent("all");
    });

    essentialOnlyBtn.addEventListener("click", function () {
        setConsent("essential");
    });

    if (manageBtn) {
        manageBtn.addEventListener("click", function () {
            showBanner();
        });
    }
});
