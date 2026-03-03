const monthName = document.getElementById("monthName");
const yearText = document.getElementById("year");
const daysContainer = document.getElementById("days");
const prevBtn = document.getElementById("prev");
const nextBtn = document.getElementById("next");

let date = new Date();

function renderCalendar() {

    const year = date.getFullYear();
    const month = date.getMonth();

    const firstDay = new Date(year, month, 1).getDay();
    const lastDate = new Date(year, month + 1, 0).getDate();

    const months = [
        "January","February","March","April","May","June",
        "July","August","September","October","November","December"
    ];

    monthName.innerText = months[month];
    yearText.innerText = year;

    daysContainer.innerHTML = "";

    // Empty spaces
    for (let i = 0; i < firstDay; i++) {
        const blank = document.createElement("div");
        daysContainer.appendChild(blank);
    }

    const today = new Date();

    for (let i = 1; i <= lastDate; i++) {

        const day = document.createElement("div");
        day.innerText = i;

        if (
            i === today.getDate() &&
            month === today.getMonth() &&
            year === today.getFullYear()
        ) {
            day.classList.add("today");
        }

        daysContainer.appendChild(day);
    }
}

prevBtn.addEventListener("click", () => {
    date.setMonth(date.getMonth() - 1);
    renderCalendar();
});

nextBtn.addEventListener("click", () => {
    date.setMonth(date.getMonth() + 1);
    renderCalendar();
});

renderCalendar();