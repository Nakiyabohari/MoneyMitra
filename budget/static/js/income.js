const salaryDisplay = document.getElementById("salaryDisplay");
const salaryReal = document.getElementById("salaryReal");

salaryDisplay.addEventListener("input", function () {

    let value = this.value.replace(/[^0-9]/g, "");

    let formatted = value.replace(/\B(?=(\d{3})+(?!\d))/g, ",");

    this.value = formatted;

    salaryReal.value = value;
});