// ---------- WELCOME PAGE ----------

document.addEventListener("DOMContentLoaded", () => {
    const button = document.getElementById("getStarted");

    if(button){
        button.addEventListener("click", () => {
            window.location.href = "login.html";
        });
    }
});

