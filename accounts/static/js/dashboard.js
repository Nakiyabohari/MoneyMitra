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


/* ================= THEME TOGGLE (IMPORTANT) ================= */
function toggleTheme(){
    document.body.classList.toggle("dark-mode");

    // 🔥 THIS FIXES EVERYTHING
    loadExpenseGraph();
}

function loadExpenseGraph() {

    let canvas = document.getElementById('expenseChart');
    if (!canvas) return;

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

    // ✅ DETECT MODE
    const isDark = document.body.classList.contains("dark-mode");

    // ✅ COLORS (FINAL CORRECT)
    const textColor = isDark ? "#ffffff" : "#000000";   // 🔥 THIS IS MAIN
    const gridColor = isDark ? "rgba(255,255,255,0.15)" : "rgba(0,0,0,0.1)";
    const lineColor = isDark ? "#a78bfa" : "#6c63ff";  // 💜 purple glow
    const fillColor = isDark 
        ? "rgba(167,139,250,0.25)" 
        : "rgba(108,99,255,0.1)";

    // ✅ DESTROY OLD CHART
    if (window.myChart) {
        window.myChart.destroy();
    }

    window.myChart = new Chart(ctx, {
        type: 'line',
        data: {
            labels: labels,
            datasets: [{
                label: 'Daily Expense',
                data: data,
                borderColor: lineColor,
                backgroundColor: fillColor,
                borderWidth: 3,
                tension: 0.4,
                fill: true,

                pointBackgroundColor: isDark ? "#ffffff" : "#000000",
                pointBorderColor: isDark ? "#000000" : "#6c63ff",
                pointBorderWidth: 2,
                pointRadius: 5
            }]
        },

        options: {
            plugins: {
                legend: {
                    labels: {
                        color: textColor   // ✅ FIXED
                    }
                }
            },

            scales: {
                x: {
                    ticks: {
                        color: textColor   // ✅ FIXED
                    },
                    grid: {
                        color: gridColor
                    }
                },
                y: {
                    ticks: {
                        color: textColor   // ✅ FIXED
                    },
                    grid: {
                        color: gridColor
                    }
                }
            }
        }
    });
}