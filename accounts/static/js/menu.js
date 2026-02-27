function open_menu() {
    document.getElementById("drawer-panel").classList.add("active");
    document.getElementById("menu-overlay").classList.add("show");
}

function close_menu() {
    document.getElementById("drawer-panel").classList.remove("active");
    document.getElementById("menu-overlay").classList.remove("show");
}

function redirect_page(url) {
    window.location.href = url;
}