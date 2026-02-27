document.addEventListener("DOMContentLoaded", function () {

    const calendar = document.getElementById("calendarDays");
    const monthTitle = document.getElementById("monthYear");
    const prevBtn = document.getElementById("prev");
    const nextBtn = document.getElementById("next");

    const months = [
        "January","February","March","April","May","June",
        "July","August","September","October","November","December"
    ];

    let currentDate = new Date();
    let currentMonth = currentDate.getMonth();
    let currentYear = currentDate.getFullYear();

    function generateCalendar(month, year) {

        calendar.innerHTML = "";
        monthTitle.textContent = `${months[month]} ${year}`;

        const firstDay = new Date(year, month, 1).getDay();
        const lastDate = new Date(year, month + 1, 0).getDate();

        // Empty spaces
        for (let i = 0; i < firstDay; i++) {
            const empty = document.createElement("div");
            calendar.appendChild(empty);
        }

        for (let day = 1; day <= lastDate; day++) {

            const dayBox = document.createElement("div");
            dayBox.textContent = day;

            // Highlight today
            const today = new Date();
            if (
                day === today.getDate() &&
                month === today.getMonth() &&
                year === today.getFullYear()
            ) {
                dayBox.classList.add("today");
            }

            // Click selection
            dayBox.addEventListener("click", function () {
                document.querySelectorAll(".days div").forEach(d => {
                    d.classList.remove("selected");
                });
                this.classList.add("selected");
            });

            calendar.appendChild(dayBox);
        }
    }

    // Month navigation
    prevBtn.addEventListener("click", function () {
        currentMonth--;
        if (currentMonth < 0) {
            currentMonth = 11;
            currentYear--;
        }
        generateCalendar(currentMonth, currentYear);
    });

    nextBtn.addEventListener("click", function () {
        currentMonth++;
        if (currentMonth > 11) {
            currentMonth = 0;
            currentYear++;
        }
        generateCalendar(currentMonth, currentYear);
    });

    generateCalendar(currentMonth, currentYear);

});