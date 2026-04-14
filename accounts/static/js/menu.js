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

function toggleTheme(){

    document.body.classList.toggle("dark-mode");

    if(document.body.classList.contains("dark-mode")){
        localStorage.setItem("theme","dark");
    }else{
        localStorage.setItem("theme","light");
    }

}

/* Load saved theme */

window.onload = function(){

    const theme = localStorage.getItem("theme");

    if(theme === "dark"){
        document.body.classList.add("dark-mode");
    }

};

document.addEventListener("DOMContentLoaded", function(){

    const toggle = document.getElementById("theme-switch");

    /* Load saved theme */

    const savedTheme = localStorage.getItem("theme");

    if(savedTheme === "dark"){
        document.body.classList.add("dark-mode");
        if(toggle) toggle.checked = true;
    }

    /* Switch theme */

    if(toggle){
        toggle.addEventListener("change", function(){

            if(this.checked){
                document.body.classList.add("dark-mode");
                localStorage.setItem("theme","dark");
            }else{
                document.body.classList.remove("dark-mode");
                localStorage.setItem("theme","light");
            }

        });
    }

});