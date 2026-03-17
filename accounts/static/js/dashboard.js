document.addEventListener("DOMContentLoaded", () => {
    loadDashboard();
});

function loadDashboard(){
    const income = Number(localStorage.getItem("income")) || 0;
    const savings = Number(localStorage.getItem("savings")) || 0;
    const investment = Number(localStorage.getItem("investmentAmount")) || 0;
    const emi = Number(localStorage.getItem("emi")) || 0;
    const addincome = Number(localStorage.getItem("addincome")) || 0;

    const balance = addincome +income - savings - investment - emi;

    document.getElementById("salaryDisplay").innerText = "₹" + income.toLocaleString();
    document.getElementById("savingsDisplay").innerText = "₹" + savings.toLocaleString();
    document.getElementById("investmentDisplay").innerText = "₹" + investment.toLocaleString();
    document.getElementById("emiDisplay").innerText = "₹" + emi.toLocaleString();
    document.getElementById("balance").innerText = "₹" + balance.toLocaleString();
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

