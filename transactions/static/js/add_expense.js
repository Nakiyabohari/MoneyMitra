
function handleCategoryChange() {
    const select = document.getElementById("categorySelect");
    const selectBox = document.getElementById("categorySelectBox");
    const inputBox = document.getElementById("categoryInputBox");

    if (select.value === "custom") {
        selectBox.classList.add("hidden");
        inputBox.classList.remove("hidden");
        document.getElementById("categoryInput").focus();
    }
}

// When user presses Enter
function handleCustomEnter(event) {
    if (event.key === "Enter") {
        event.preventDefault();
        finalizeCustomCategory();
    }
}

function finalizeCustomCategory() {
    const input = document.getElementById("categoryInput");
    const value = input.value.trim();
    const select = document.getElementById("categorySelect");
    const selectBox = document.getElementById("categorySelectBox");
    const inputBox = document.getElementById("categoryInputBox");

    if (value === "") {
        // If empty → go back to dropdown
        inputBox.classList.add("hidden");
        selectBox.classList.remove("hidden");
        select.value = "";
        return;
    }

    // Remove existing custom options (avoid duplicates)
    const existingOption = document.getElementById("dynamicCustomOption");
    if (existingOption) {
        existingOption.remove();
    }

    // Create new option
    const newOption = document.createElement("option");
    newOption.value = value;
    newOption.text = value;
    newOption.selected = true;
    newOption.id = "dynamicCustomOption";

    select.appendChild(newOption);

    // Switch back to dropdown
    inputBox.classList.add("hidden");
    selectBox.classList.remove("hidden");
}
