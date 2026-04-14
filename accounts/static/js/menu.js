/* APPLY SAVED THEME BEFORE PAGE LOAD */
(function () {
    const savedTheme = localStorage.getItem("theme");
    if (savedTheme === "dark") {
        document.body.classList.add("dark-mode");
    }
})();

/* AFTER PAGE LOAD */
document.addEventListener("DOMContentLoaded", function () {

    const toggle = document.getElementById("themeSwitch");
    const isDark = document.body.classList.contains("dark-mode");

    // SET SWITCH STATE
    if (toggle) toggle.checked = isDark;

    // HANDLE TOGGLE
    if (toggle) {
        toggle.addEventListener("change", function () {

            if (this.checked) {
                document.body.classList.add("dark-mode");
                localStorage.setItem("theme", "dark");
            } else {
                document.body.classList.remove("dark-mode");
                localStorage.setItem("theme", "light");
            }

        });
    }

});