document.addEventListener("DOMContentLoaded", function () {

    const inputs = document.querySelectorAll("form input");

    inputs.forEach(input => {
        input.addEventListener("focus", function () {
            this.style.borderColor = "#6a5acd";
        });

        input.addEventListener("blur", function () {
            this.style.borderColor = "#ddd";
        });
    });

});