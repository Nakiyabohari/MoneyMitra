// LIVE AMOUNT DISPLAY
document.addEventListener("DOMContentLoaded", function () {
    const amountInput = document.getElementById("amountInput");
    const displayAmount = document.getElementById("displayAmount");

    amountInput.addEventListener("input", function () {
        displayAmount.innerText = "₹" + (this.value || 0);
    });
});

function handleSourceChange() {
    const select = document.getElementById("incomeSourceSelect");
    const input = document.getElementById("customSourceInput");

    if (select.value === "Other") {
        select.classList.add("hidden");
        input.classList.remove("hidden");
        input.focus();
    }
}

function handleCustomEnter(event) {
    if (event.key === "Enter") {
        event.preventDefault();
        finalizeCustomSource();
    }
}

function finalizeCustomSource() {
    const input = document.getElementById("customSourceInput");
    const select = document.getElementById("incomeSourceSelect");
    const value = input.value.trim();

    if (value === "") {
        input.classList.add("hidden");
        select.classList.remove("hidden");
        select.value = "";
        return;
    }

    const oldOption = document.getElementById("dynamicIncomeOption");
    if (oldOption) oldOption.remove();

    const newOption = document.createElement("option");
    newOption.value = value;
    newOption.text = value;
    newOption.id = "dynamicIncomeOption";

    select.appendChild(newOption);
    select.value = value;

    input.value = "";
    input.classList.add("hidden");
    select.classList.remove("hidden");
}