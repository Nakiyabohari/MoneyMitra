document.addEventListener("DOMContentLoaded", function () {

    const select = document.getElementById("categorySelect");
    const inputBox = document.getElementById("categoryInputBox");
    const input = document.getElementById("categoryInput");

    select.addEventListener("change", function () {

        if (this.value === "custom") {
            inputBox.classList.remove("hidden");
            input.focus();
        } else {
            inputBox.classList.add("hidden");
        }

    });

    input.addEventListener("keydown", function (event) {

        if (event.key === "Enter") {
            event.preventDefault();

            const value = input.value.trim();
            if (!value) return;

            const existing = document.getElementById("dynamicCustomOption");
            if (existing) existing.remove();

            const newOption = document.createElement("option");
            newOption.value = value;
            newOption.text = value;
            newOption.id = "dynamicCustomOption";
            newOption.selected = true;

            select.appendChild(newOption);

            input.value = "";
            inputBox.classList.add("hidden");
        }

    });

});