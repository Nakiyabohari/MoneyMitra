/* =========================
GET DATA FROM DJANGO
========================= */

const data = summaryData;

const investments = data.investments;
const savings = data.savings;
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
const month = String(today.getMonth() + 1).padStart(2,"0");

// set current month
monthPicker.value = `${year}-${month}`;

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
investments + savings + emi + balance;

let startAngle = -Math.PI / 2;

const slices = [

{value:investments,color:"#6C63FF"},
{value:savings,color:"#00b894"},
{value:emi,color:"#fdcb6e"},
{value:balance,color:"#e8e6ff"}

];

ctx.clearRect(0,0,200,200);

slices.forEach(slice=>{

if(slice.value === 0) return;

const angle =
(slice.value / total) * Math.PI * 2;

ctx.beginPath();

ctx.arc(
100,
100,
70,
startAngle,
startAngle + angle
);

ctx.strokeStyle = slice.color;
ctx.lineWidth = 14;

ctx.stroke();

startAngle += angle;

});

}

drawDonut();