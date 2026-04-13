document.addEventListener("DOMContentLoaded", function () {

    /* =========================
    SAFETY CHECK
    ========================== */

    if (typeof labels === "undefined" || labels.length === 0) {
        console.log("No chart data available");
        return;
    }

    console.log("Labels:", labels);
    console.log("Budget Data:", budgetData);
    console.log("Spent Data:", spentData);


    /* =========================
    PIE CHART - SPENDING BY CATEGORY
    ========================== */

    const pieCanvas = document.getElementById("categoryChart");

if (pieCanvas) {

new Chart(pieCanvas,{
type:"pie",

data:{
labels:labels,
datasets:[{
data:spentData,

backgroundColor:[
"#4C3FE0",   // deep purple
"#6C5CE7",   // main purple
"#8E7BFF",   // medium purple
"#A99CFF",   // light purple
"#C6BEFF"    // soft purple
],

hoverBackgroundColor:[
"#3B2ED4",
"#5A49E6",
"#7B67FF",
"#9B8FFF",
"#B8AEFF"
],

borderColor:"#ffffff",
borderWidth:3
}]
},

options:{
responsive:true,
maintainAspectRatio:false,

plugins:{
legend:{
position:"bottom",

labels:{
boxWidth:20,
padding:18,
font:{
size:14,
weight:"500"
}
}
},

tooltip:{
callbacks:{
label:function(context){
return context.label + ": ₹" + context.raw;
}
}
}
},

animation:{
animateRotate:true,
duration:800
}
}

});

}

    /* =========================
       BAR CHART - BUDGET VS SPENDING
    ========================== */

    const budgetCanvas = document.getElementById("budgetChart");

if (budgetCanvas) {

    new Chart(budgetCanvas, {
        type: "bar",
        data: {
            labels: labels,
            datasets: [
                {
                    label: "Budget",
                    data: budgetData,
                    backgroundColor: "rgba(108, 92, 231, 0.25)",
                    borderRadius: 10,
                    barThickness: 35
                },
                {
                    label: "Spent",
                    data: spentData,
                    backgroundColor: "#6C5CE7",
                    borderRadius: 10,
                    barThickness: 20
                }
            ]
        },
        options: {
            responsive: true,
            plugins: {
                legend: {
                    position: "bottom"
                },
                tooltip: {
                    callbacks: {
                        label: function(context) {
                            return context.dataset.label + ": ₹" + context.raw;
                        }
                    }
                }
            },
            scales: {
                y: {
                    beginAtZero: true,
                    ticks: {
                        callback: function(value) {
                            if (value >= 1000) {
                                return "₹" + value/1000 + "k";
                            }
                            return "₹" + value;
                        }
                    }
                }
            }
        }
    });

}

});