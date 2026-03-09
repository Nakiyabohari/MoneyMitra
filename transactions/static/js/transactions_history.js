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

                <button class="action-btn edit"
                data-id="${t.id}"
                data-model="${t.model}"
                data-amount="${t.amount}"
                data-title="${t.title}">
                ✏
                </button>

                <button class="action-btn delete"
                data-id="${t.id}"
                data-model="${t.model}">
                🗑
                </button>

            </div>

        </div>
        `;

        list.appendChild(item);

    });

    attachDeleteEvents();
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



/* ================= DELETE ================= */

function attachDeleteEvents() {

    document.querySelectorAll(".delete").forEach(btn => {

        btn.addEventListener("click", function () {

            const id = this.dataset.id;
            const model = this.dataset.model;

            if (!confirm("Delete this transaction?")) return;

            fetch("/transactions/delete-transaction/", {
                method: "POST",
                headers: {
                    "Content-Type": "application/x-www-form-urlencoded",
                    "X-CSRFToken": getCookie("csrftoken")
                },
                body: `id=${id}&model=${model}`
            })
            .then(res => res.json())
            .then(data => {
                console.log("DELETE RESPONSE:", data);
                location.reload();
            })
            .catch(error => console.log("ERROR:", error));

        });

    });

}



/* ================= CSRF ================= */

function getCookie(name) {
    let cookieValue = null;

    if (document.cookie && document.cookie !== "") {

        const cookies = document.cookie.split(";");

        for (let i = 0; i < cookies.length; i++) {

            const cookie = cookies[i].trim();

            if (cookie.substring(0, name.length + 1) === (name + "=")) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }

        }
    }

    return cookieValue;
}



/* ================= EDIT MODAL ================= */

document.addEventListener("click", function(e){

if(e.target.classList.contains("edit")){

    const modal = document.getElementById("editModal");

    modal.style.display = "flex";

    document.getElementById("editId").value = e.target.dataset.id;
    document.getElementById("editModel").value = e.target.dataset.model;
    document.getElementById("editAmount").value = e.target.dataset.amount;
    document.getElementById("editCategory").value = e.target.dataset.title;

}

});

/* CLOSE MODAL */

document.querySelector(".close-edit").onclick = () =>{
    modal.style.display="none";
};



/* ================= SAVE EDIT ================= */

document.getElementById("saveEdit").addEventListener("click", function(){

    const id = document.getElementById("editId").value;
    const model = document.getElementById("editModel").value;
    const amount = document.getElementById("editAmount").value;
    const category = document.getElementById("editCategory").value;
    const notes = document.getElementById("editNotes").value;

    fetch("/transactions/edit-transaction/", {

        method: "POST",

        headers:{
            "Content-Type":"application/x-www-form-urlencoded",
            "X-CSRFToken":getCookie("csrftoken")
        },

        body:`id=${id}&model=${model}&amount=${amount}&category=${category}&notes=${notes}`

    })
    .then(res => res.json())
    .then(data => {

        console.log("EDIT RESPONSE:", data);

        if(data.status === "success"){
            location.reload();
        }

    })
    .catch(error => console.log("ERROR:", error));

});