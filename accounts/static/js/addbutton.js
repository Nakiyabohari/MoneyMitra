// elements
const overlay = document.querySelector(".page-overlay");
const sheet = document.querySelector(".bottom-sheet");

// OPEN
function openSheet() {
    overlay.classList.add("active");
    sheet.classList.add("active");
    document.body.classList.add("no-scroll");
}

// CLOSE
function closeSheet() {
    overlay.classList.remove("active");
    sheet.classList.remove("active");
    document.body.classList.remove("no-scroll");
}

// REDIRECT (🔥 FIXED NAME)
function redirect_page(route) {
    window.location.href = route;
}