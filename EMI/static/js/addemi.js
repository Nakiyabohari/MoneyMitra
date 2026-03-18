document.addEventListener("DOMContentLoaded", function () {

    const startDate = document.querySelector('input[name="start_date"]');
    const duration = document.querySelector('input[name="duration"]');
    const endDate = document.querySelector('input[name="end_date"]');
    const form = document.querySelector("form");

    if (endDate) {
        endDate.readOnly = true;
    }

    function calculateEndDate() {

        if (!startDate.value || !duration.value) return;

        let start = new Date(startDate.value);
        let months = parseInt(duration.value);

        if (isNaN(months)) return;

        start.setMonth(start.getMonth() + months);

        let dd = String(start.getDate()).padStart(2, "0");
        let mm = String(start.getMonth() + 1).padStart(2, "0");
        let yyyy = start.getFullYear();

        // show formatted
        endDate.value = `${dd}-${mm}-${yyyy}`;
    }

    duration.addEventListener("input", calculateEndDate);
    startDate.addEventListener("change", calculateEndDate);

    // 🔥 Convert ONLY end_date before submit
    form.addEventListener("submit", function () {

        if (endDate.value.includes("-")) {
            let parts = endDate.value.split("-");
            if (parts.length === 3) {
                endDate.value = `${parts[2]}-${parts[1]}-${parts[0]}`;
            }
        }
    });

});