let display = document.getElementById("display");

let currentInput = "0";

function updateDisplay() {
    display.innerText = currentInput;
}

function append(value) {
    if (currentInput === "0") {
        currentInput = value;
    } else {
        currentInput += value;
    }
    updateDisplay();
}

function clearDisplay() {
    currentInput = "0";
    updateDisplay();
}

function deleteLast() {
    currentInput = currentInput.slice(0, -1);

    if (currentInput === "") {
        currentInput = "0";
        }
        updateDisplay();
}

function calculate() {
        try {
        currentInput = eval(currentInput).toString();
        }
        catch {
        currentInput = "Error";
        }
        updateDisplay();
}