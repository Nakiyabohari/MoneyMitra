
// Set today's date default
document.getElementById("date").valueAsDate = new Date();

function goBack() {
    alert("Back button clicked");
}

function saveExpense() {

    const expense = {
        amount: document.getElementById("amount").value,
        category: document.getElementById("category").value,
        date: document.getElementById("date").value,
        payment: document.getElementById("payment").value,
        notes: document.getElementById("notes").value
    };

    if (!expense.amount || !expense.category || !expense.payment) {
        alert("Please fill required fields");
        return;
    }

    console.log("Expense Saved:", expense);

    alert("Expense Saved Successfully!👍🏻🤩");

    // Clear form
    document.getElementById("amount").value = "";
    document.getElementById("category").value = "";
    document.getElementById("payment").value = "";
    document.getElementById("notes").value = "";
}
