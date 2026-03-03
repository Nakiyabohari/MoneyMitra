/* Live amount display */
document.getElementById("amountInput").addEventListener("input", function () {
    const value = this.value || 0;
    document.getElementById("displayAmount").innerText = "₹" + value;
});

/* Handle dropdown change */
function handleSourceChange() {
    const select = document.getElementById("incomeSourceSelect");
    const selectBox = document.getElementById("sourceSelectBox");
    const inputBox = document.getElementById("sourceInputBox");

    if (select.value === "Other") {
        selectBox.classList.add("hidden");
        inputBox.classList.remove("hidden");
        document.getElementById("customSourceInput").focus();
    }
}

/* When user presses Enter */
function handleCustomEnter(event) {
    if (event.key === "Enter") {
        event.preventDefault();
        finalizeCustomSource();
    }
}

/* Finalize custom source */
function finalizeCustomSource() {
    const input = document.getElementById("customSourceInput");
    const value = input.value.trim();
    const select = document.getElementById("incomeSourceSelect");
    const selectBox = document.getElementById("sourceSelectBox");
    const inputBox = document.getElementById("sourceInputBox");

    if (value === "") {
        inputBox.classList.add("hidden");
        selectBox.classList.remove("hidden");
        select.value = "";
        return;
    }

    // Remove previous dynamic option if exists
    const oldOption = document.getElementById("dynamicIncomeOption");
    if (oldOption) oldOption.remove();

    const newOption = document.createElement("option");
    newOption.value = value;
    newOption.text = value;
    newOption.selected = true;
    newOption.id = "dynamicIncomeOption";

    select.appendChild(newOption);

    inputBox.classList.add("hidden");
    selectBox.classList.remove("hidden");
}