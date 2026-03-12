document.addEventListener("DOMContentLoaded", function () {

    const inputs = document.querySelectorAll("form input");

    inputs.forEach(input => {
        input.addEventListener("focus", function () {
            this.style.borderColor = "#6a5acd";
        });

        input.addEventListener("blur", function () {
            this.style.borderColor = "#ddd";
        });
    });

});

document.addEventListener("DOMContentLoaded", function () {

    const startDate = document.querySelector('input[name="start_date"]');
    const duration = document.querySelector('input[name="duration"]');
    const endDate = document.querySelector('input[name="end_date"]');

    if (endDate) {
        endDate.readOnly = true;
    }

    function calculateEndDate() {

        if (!startDate.value || !duration.value) return;

        // Browser date input already gives yyyy-mm-dd
        let start = new Date(startDate.value);

        let months = parseInt(duration.value);

        start.setMonth(start.getMonth() + months);

        let dd = String(start.getDate()).padStart(2, "0");
        let mm = String(start.getMonth() + 1).padStart(2, "0");
        let yyyy = start.getFullYear();

        endDate.value = `${dd}-${mm}-${yyyy}`;
    }

    duration.addEventListener("input", calculateEndDate);
    startDate.addEventListener("change", calculateEndDate);

});