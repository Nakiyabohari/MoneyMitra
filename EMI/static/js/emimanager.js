document.addEventListener("DOMContentLoaded", function () {

    calculateTotal();
    checkEmiStatus();

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

function checkEmiStatus() {

    const emiCards = document.querySelectorAll(".emi-card");
    const today = new Date();
    today.setHours(0,0,0,0); // remove time part

    emiCards.forEach(function(card) {

        const endDateString = card.getAttribute("data-end");

        if (!endDateString) return;

        const endDate = new Date(endDateString);
        const statusElement = card.querySelector(".status");

        if (today >= endDate) {

            statusElement.innerText = "Inactive";
            statusElement.style.color = "red";
            statusElement.style.fontWeight = "bold";

        } else {

            statusElement.innerText = "Active";
            statusElement.style.color = "green";
            statusElement.style.fontWeight = "bold";

        }

    });

}