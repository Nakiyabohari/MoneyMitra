/* =========================
GET DATA FROM DJANGO
========================= */

const data = summaryData;

const investments = data.investments;
const savings = data.savings;
const expense = data.expense;
const emi = data.emi;
const balance = data.balance;


/* =========================
CALENDAR SETTINGS
ONLY CURRENT YEAR
========================= */

const monthPicker = document.getElementById("monthPicker");

if (monthPicker){

const today = new Date();

const year = today.getFullYear();

// allow only current year
monthPicker.min = `${year}-01`;
monthPicker.max = `${year}-12`;

}


/* =========================
SUGGESTED DAILY SPENDING
========================= */

const dailyLimit = Math.floor(balance / 30);

const dailyElement = document.getElementById("dailyLimit");

if(dailyElement){

dailyElement.innerHTML =
`₹${dailyLimit.toLocaleString("en-IN")} <span>/ day</span>`;

}


/* =========================
DONUT CHART
========================= */

const canvas = document.getElementById("donutChart");
const ctx = canvas.getContext("2d");

function drawDonut(){

const total =
investments + savings + expense + emi + balance;

let startAngle = -Math.PI / 2;

ctx.clearRect(0,0,200,200);

// 🔥 gradient creator (main purple style)
function getGradient(startColor, endColor){
    const gradient = ctx.createLinearGradient(0,0,200,200);
    gradient.addColorStop(0, startColor);
    gradient.addColorStop(1, endColor);
    return gradient;
}

const slices = [

{ value: Math.max(investments, 0), gradient: getGradient("#6C5CE7", "#B76DF7") },
{ value: Math.max(expense, 0),     gradient: getGradient("#A29BFE", "#D6CCFF") },
{ value: Math.max(savings, 0),     gradient: getGradient("#8E7CFF", "#C3B6FF") },
{ value: Math.max(emi, 0),         gradient: getGradient("#7B6CF6", "#B3A6FF") },
{ value: Math.max(balance, 0),     gradient: getGradient("#5A4FCF", "#9B8CFF") }

];

slices.forEach(slice => {

    if(slice.value === 0) return;

    const angle = (slice.value / total) * Math.PI * 2;

    ctx.beginPath();

    ctx.arc(
        100,
        100,
        75,              // 🔥 slightly bigger radius
        startAngle,
        startAngle + angle
    );

    ctx.strokeStyle = slice.gradient;

    ctx.lineWidth = 22;   // 🔥 THICK ring like your image
    ctx.lineCap = "butt"; // clean segment edges

    ctx.stroke();

    startAngle += angle;

});


}

drawDonut();


/* =========================
MONTH CHANGE -> FETCH DATA
========================= */

if(monthPicker){

monthPicker.addEventListener("change", function(){

const selectedMonth = this.value;

// reload page with selected month
window.location.href = `?month=${selectedMonth}`;

});

}