const amountInput = document.getElementById("amountInput");
const displayAmount = document.getElementById("displayAmount");
const form = document.getElementById("incomeForm");
const successMsg = document.getElementById("successMsg");

/* Live amount update */
amountInput.addEventListener("input", function(){
    let value = amountInput.value;
    if(value === "" || value <= 0){
        displayAmount.textContent = "₹0";
    } else {
        displayAmount.textContent = "₹" + parseFloat(value).toLocaleString("en-IN");
    }
});

/* Form Submit */
form.addEventListener("submit", function(e){
    e.preventDefault();

    const amount = amountInput.value;
    const source = document.getElementById("sourceInput").value;
    const payment = document.getElementById("paymentInput").value;

    if(amount <= 0){
        alert("Please enter valid amount");
        return;
    }

    if(source === "" || payment === ""){
        alert("Please select all required fields");
        return;
    }

    // Example: Save to localStorage
    let incomes = JSON.parse(localStorage.getItem("incomes")) || [];
    incomes.push({
        amount,
        source,
        payment,
        notes: document.getElementById("notesInput").value,
        date: new Date().toLocaleDateString()
    });

    localStorage.setItem("incomes", JSON.stringify(incomes));

    successMsg.style.display = "block";
    form.reset();
    displayAmount.textContent = "₹0";

    setTimeout(() => {
        successMsg.style.display = "none";
    }, 2000);
});