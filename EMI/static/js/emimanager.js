document.addEventListener("DOMContentLoaded", function () {

    calculateTotal();

});

function calculateTotal() {

    const amountElements = document.querySelectorAll(".emi-amount");
    let total = 0;

    amountElements.forEach(function (item) {

        let value = item.innerText
            .replace("₹", "")
            .replace("/month", "")
            .replace(/,/g, "")
            .trim();

        if (value) {
            total += parseFloat(value);
        }

    });

    const totalElement = document.getElementById("totalEmi");

    if (totalElement) {
        totalElement.innerText = "₹" + total.toLocaleString();
    }
}