const dataElement = document.getElementById("transactions-data");

console.log("DATA ELEMENT:", dataElement);

let transactions = [];

if (dataElement) {
    transactions = JSON.parse(dataElement.textContent);
}

console.log("TRANSACTIONS FROM DJANGO:", transactions);

const list = document.getElementById("transactionList");

function renderTransactions() {

    list.innerHTML = "";

    if (transactions.length === 0) {
        list.innerHTML = "<p style='text-align:center;'>No transactions found</p>";
        return;
    }

    transactions.forEach(t => {

        const item = document.createElement("div");

        item.classList.add("transaction");
        item.classList.add(t.type);

        item.innerHTML = `
        <div class="title">${t.title}</div>
        <div class="date">${t.date}</div>
        <div class="amount">₹${t.amount}</div>
        `;

        list.appendChild(item);

    });

}

renderTransactions();