document.addEventListener("DOMContentLoaded", () => {
    loadDashboard();
});

function loadDashboard(){
    
    const savings = Number(localStorage.getItem("savings")) || 0;
    const investment = Number(localStorage.getItem("investmentAmount")) || 0;
    const emi = Number(localStorage.getItem("emi")) || 0;
    const addincome = Number(localStorage.getItem("addincome")) || 0;
    const income = Number(localStorage.getItem("income")) || 0;
    const balance = addincome +income - savings - investment - emi;

    document.getElementById("salaryDisplay").innerText = "₹" + income.toLocaleString();
    document.getElementById("savingsDisplay").innerText = "₹" + savings.toLocaleString();
    document.getElementById("investmentDisplay").innerText = "₹" + investment.toLocaleString();
    document.getElementById("emiDisplay").innerText = "₹" + emi.toLocaleString();
    document.getElementById("balance").innerText = "₹" + balance.toLocaleString();

    loadExpenseGraph();
}

function openQuickAdd(){
    document.getElementById("quickAddModal").classList.add("active");
    document.getElementById("quickAddOverlay").classList.add("active");
}

function closeQuickAdd(){
    document.getElementById("quickAddModal").classList.remove("active");
    document.getElementById("quickAddOverlay").classList.remove("active");
}

function addIncome(){
    let amount = prompt("Enter Income:");
    if(amount){
        localStorage.setItem("income", amount);
        loadDashboard();
        closeQuickAdd();
    }
}

function addSavings(){
    let amount = prompt("Enter Savings:");
    if(amount){
        localStorage.setItem("savings", amount);
        loadDashboard();
        closeQuickAdd();
    }
}

function addInvestment(){
    let amount = prompt("Enter Investment:");
    if(amount){
        localStorage.setItem("investmentAmount", amount);
        loadDashboard();
        closeQuickAdd();
    }
}

function addEMI(){
    let amount = prompt("Enter EMI:");
    if(amount){
        localStorage.setItem("emi", amount);
        loadDashboard();
        closeQuickAdd();
    }
}

function goToCalculator(){
    window.location.href="calculator.html";
}

function goToCalendar(){
    window.location.href="calendar.html";
}

function goToSavings(){
    window.location.href="savings.html";
}

function goToInvestment(){
    window.location.href="investment.html";
}

function goToEMI(){
    window.location.href="emi.html";
}
function open_menu(){
document.getElementById("drawer-panel").classList.add("active");
document.getElementById("menu-overlay").classList.add("show");
}

function close_menu(){
document.getElementById("drawer-panel").classList.remove("active");
document.getElementById("menu-overlay").classList.remove("show");
}

function openQuickAdd(){
document.getElementById("quick-sheet").classList.add("active");
document.getElementById("quick-overlay").classList.add("active");
}

function closeQuickAdd(){
document.getElementById("quick-sheet").classList.remove("active");
document.getElementById("quick-overlay").classList.remove("active");
}


function loadExpenseGraph() {

    let canvas = document.getElementById('expenseChart');
    if (!canvas) return; // 🔥 prevent error

    let expenses = expensesData || [];

    let dailyData = {};

    expenses.forEach(exp => {
        if (dailyData[exp.date]) {
            dailyData[exp.date] += exp.amount;
        } else {
            dailyData[exp.date] = exp.amount;
        }
    });

    let labels = Object.keys(dailyData);
    let data = Object.values(dailyData);

    const ctx = canvas.getContext('2d');

    new Chart(ctx, {
    type: 'line',
    data: {
        labels: labels,
        datasets: [{
            label: 'Daily Expense',
            data: data,

            borderColor: "#6c63ff",
            backgroundColor: "rgba(108,99,255,0.15)",
            borderWidth: 3,

            tension: 0.4,
            fill: true,

            pointBackgroundColor: "#ffffff",
            pointBorderColor: "#6c63ff",
            pointRadius: 5,
            pointHoverRadius: 7
        }]
    },

    options: {
        plugins: {
            legend: {
                labels: {
                    color: "#1f1f3d",
                    font: {
                        size: 14,
                        weight: "600"
                    }
                }
            }
        },

        scales: {
            x: {
                ticks: {
                    color: "#6f6f9f"
                },
                grid: {
                    color: "rgba(0,0,0,0.05)"
                }
            },
            y: {
                ticks: {
                    color: "#6f6f9f"
                },
                grid: {
                    color: "rgba(0,0,0,0.05)"
                }
            }
        }
    }
});
}