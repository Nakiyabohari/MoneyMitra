// Check if script loaded
console.log("Expense report JS loaded");

document.addEventListener("DOMContentLoaded", function () {

    if (!window.reportData) {
        console.error("reportData not found");
        return;
    }

    const incomes = window.reportData.incomes || [];
    const expenses = window.reportData.expenses || [];
    const totalIncome = window.reportData.totalIncome || 0;
    const totalExpense = window.reportData.totalExpense || 0;
    const balance = window.reportData.balance || 0;

    const downloadBtn = document.getElementById("downloadBtn");
    const shareBtn = document.getElementById("shareBtn");

    if (downloadBtn) {
        downloadBtn.addEventListener("click", downloadPDF);
    }

    if (shareBtn) {
        shareBtn.addEventListener("click", sharePDF);
    }

    function generatePDFBlob() {

        const { jsPDF } = window.jspdf;
        const doc = new jsPDF();

        const month = document.getElementById("monthSelect")?.value || "";
        const year = document.getElementById("yearSelect")?.value || "";

        let y = 20;

        doc.setFontSize(18);
        doc.text("Expense Report", 105, y, { align: "center" });
        y += 10;

        doc.text(`Period: ${month} ${year}`, 20, y);
        y += 10;

        doc.text("INCOME", 20, y);
        y += 10;

        incomes.forEach(item => {
            doc.text(item.source || "", 20, y);
            doc.text("Rs " + (item.amount || 0), 190, y, { align: "right" });
            y += 8;
        });

        y += 5;
        doc.text("Total Income: Rs " + totalIncome, 20, y);
        y += 15;

        doc.text("EXPENSE", 20, y);
        y += 10;

        expenses.forEach(item => {
            doc.text(item.category || "", 20, y);
            doc.text("Rs " + (item.amount || 0), 190, y, { align: "right" });
            y += 8;
        });

        y += 5;
        doc.text("Total Expense: Rs " + totalExpense, 20, y);
        y += 15;

        doc.text("Balance: Rs " + balance, 20, y);

        return doc.output("blob");
    }

    function downloadPDF() {

        const blob = generatePDFBlob();
        const month = document.getElementById("monthSelect")?.value || "";
        const year = document.getElementById("yearSelect")?.value || "";

        const link = document.createElement("a");
        link.href = URL.createObjectURL(blob);
        link.download = `Expense_${month}_${year}.pdf`;
        link.click();
    }

    async function sharePDF() {

        const blob = generatePDFBlob();
        const file = new File([blob], "Expense_Report.pdf", { type: "application/pdf" });

        if (navigator.canShare && navigator.canShare({ files: [file] })) {

            await navigator.share({
                title: "Expense Report",
                files: [file]
            });

        } else {
            downloadPDF();
            alert("Sharing not supported. File downloaded instead.");
        }
    }

});