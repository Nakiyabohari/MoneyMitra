function generatePDFBlob(){

const { jsPDF } = window.jspdf;
const doc = new jsPDF();

const month = document.getElementById("monthSelect").value;
const year = document.getElementById("yearSelect").value;
const today = new Date().toLocaleDateString("en-GB");

let y = 20;

doc.setFontSize(22);
doc.text("MoneyMitra",105,y,{align:"center"});
y+=12;

doc.setFontSize(18);
doc.text("Expense Report",105,y,{align:"center"});
y+=15;

doc.setFontSize(12);
doc.text(`Period: ${month} ${year}`,20,y);
doc.text(`Date: ${today}`,190,y,{align:"right"});
y+=10;

doc.text("INCOME",20,y);
y+=10;

incomes.forEach(income=>{
  doc.text(income.source,20,y);
  doc.text("Rs "+income.amount,190,y,{align:"right"});
  y+=10;
});

doc.text("Total Income",20,y);
doc.text("Rs "+totalIncome,190,y,{align:"right"});
y+=15;

doc.text("EXPENSE",20,y);
y+=10;

expenses.forEach(expense=>{
  doc.text(expense.category,20,y);
  doc.text("Rs "+expense.amount,190,y,{align:"right"});
  y+=10;
});

doc.text("Total Expense",20,y);
doc.text("Rs "+totalExpense,190,y,{align:"right"});
y+=15;

doc.text("Balance",20,y);
doc.text("Rs "+balance,190,y,{align:"right"});

return doc.output("blob");
}



function downloadPDF(){

const blob = generatePDFBlob();

const month = document.getElementById("monthSelect").value;
const year = document.getElementById("yearSelect").value;

const fileName = `MoneyMitra_${month}_${year}.pdf`;

const link = document.createElement("a");
link.href = URL.createObjectURL(blob);
link.download = fileName;
link.click();

}



async function sharePDF(){

const blob = generatePDFBlob();

const month = document.getElementById("monthSelect").value;
const year = document.getElementById("yearSelect").value;

const file = new File(
[blob],
`MoneyMitra_${month}_${year}.pdf`,
{ type:"application/pdf" }
);

if(navigator.canShare &&
navigator.canShare({files:[file]})){

await navigator.share({
title:"MoneyMitra Report",
text:"My Expense Report",
files:[file]
});

}
else{
downloadPDF();
alert("Sharing not supported. File downloaded.");
}

}