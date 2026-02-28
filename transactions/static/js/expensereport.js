
function goBack() {
  window.history.back();
}
function downloadPDF() {

  const { jsPDF } = window.jspdf;
  const doc = new jsPDF("p", "mm", "a4");

  const month = document.getElementById("month").value;
  const year = document.getElementById("year").value;

  const today = new Date();
  const formattedDate =
    String(today.getDate()).padStart(2, '0') + "/" +
    String(today.getMonth() + 1).padStart(2, '0') + "/" +
    today.getFullYear();

  const pageWidth = doc.internal.pageSize.getWidth();
  let y = 20;

  // ===== HEADER =====
  doc.setFont("helvetica", "bold");
  doc.setFontSize(22);
  doc.text("MoneyMitra", pageWidth / 2, y, { align: "center" });

  y += 10;
  doc.setFontSize(16);
  doc.text("Monthly Expense Report", pageWidth / 2, y, { align: "center" });

  y += 15;
  doc.setFontSize(12);
  doc.setFont("helvetica", "normal");

  doc.text(`Report Period: ${month} ${year}`, 20, y);
  doc.text(`Generated on: ${formattedDate}`, pageWidth - 20, y, { align: "right" });

  y += 5;
  doc.line(20, y, pageWidth - 20, y);

  // ===== INCOME SUMMARY =====
  y += 15;
  doc.setFont("helvetica", "bold");
  doc.setFontSize(14);
  doc.text("INCOME SUMMARY", 20, y);

  y += 10;
  doc.setFont("helvetica", "normal");
  doc.setFontSize(13);

  doc.text("Monthly Salary", 20, y);
  doc.text("Rs.78,97,89,789", pageWidth - 20, y, { align: "right" });

  y += 10;
  doc.text("Other Income", 20, y);
  doc.text("Rs.0", pageWidth - 20, y, { align: "right" });

  y += 10;
  doc.text("Total Income", 20, y);
  doc.text("Rs.78,97,89,789", pageWidth - 20, y, { align: "right" });

  // ===== EXPENSE SUMMARY =====
  y += 20;
  doc.setFont("helvetica", "bold");
  doc.setFontSize(14);
  doc.text("EXPENSE SUMMARY", 20, y);

  y += 10;
  doc.setFont("helvetica", "normal");
  doc.setFontSize(13);

  doc.text("Total Expenses", 20, y);
  doc.text("Rs.0", pageWidth - 20, y, { align: "right" });

  y += 10;
  doc.text("Investments", 20, y);
  doc.text("Rs.0", pageWidth - 20, y, { align: "right" });

  y += 10;
  doc.text("Net Balance", 20, y);
  doc.text("Rs.78,97,89,789", pageWidth - 20, y, { align: "right" });

  // ===== SAVE =====
  doc.save(`MoneyMitra_Report_${month}_${year}.pdf`);
}