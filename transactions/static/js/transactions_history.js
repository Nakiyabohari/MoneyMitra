const dataElement = document.getElementById("transactions-data");

let transactions = [];

if (dataElement) {
    transactions = JSON.parse(dataElement.textContent);
}

const list = document.getElementById("transactionList");
const searchInput = document.getElementById("search");
const typeFilter = document.getElementById("typeFilter");


function renderTransactions(data) {

    list.innerHTML = "";

    if (data.length === 0) {
        list.innerHTML = "<p style='text-align:center;'>No transactions found</p>";
        return;
    }

    data.forEach(t => {

        const item = document.createElement("div");
        item.classList.add("transaction");

        item.innerHTML = `

        <div class="transaction-left">

            <div class="icon ${t.type}">
                ↗
            </div>

            <div class="texts">
                <div class="title">${t.title}</div>
                <div class="sub">${t.date} • UPI</div>
            </div>

        </div>


        <div class="transaction-right">

            <div class="amount ${t.type}">
                ${t.type === "income" ? "+" : "-"}₹${t.amount}
            </div>

            <div class="actions">
                <button class="action-btn edit">✏</button>
                <button class="action-btn delete">🗑</button>
            </div>

        </div>

        `;

        list.appendChild(item);

    });

}


function filterTransactions() {

    const searchValue = searchInput.value.toLowerCase();
    const typeValue = typeFilter.value;

    const filtered = transactions.filter(t => {

        const matchSearch = t.title.toLowerCase().includes(searchValue);

        const matchType =
            typeValue === "all" || t.type === typeValue;

        return matchSearch && matchType;

    });

    renderTransactions(filtered);
}

searchInput.addEventListener("keyup", filterTransactions);
typeFilter.addEventListener("change", filterTransactions);

renderTransactions(transactions);