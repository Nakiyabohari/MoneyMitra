document.addEventListener("DOMContentLoaded", function () {

    if (!window.reportData || !window.jspdf) {
        console.error("Required data or jsPDF missing");
        return;
    }

    const { jsPDF } = window.jspdf;

    const incomes = window.reportData.incomes || [];
    const expenses = window.reportData.expenses || [];
    const totalIncome = window.reportData.totalIncome || 0;
    const totalExpense = window.reportData.totalExpense || 0;
    const balance = window.reportData.balance || 0;

    const downloadBtn = document.getElementById("downloadBtn");
    const shareBtn = document.getElementById("shareBtn");

    function formatCurrency(amount) {
        return "Rs. " + Number(amount).toLocaleString("en-IN");
    }

    function generatePDFBlob() {

        const doc = new jsPDF();
        const pageWidth = doc.internal.pageSize.getWidth();

        const month = document.getElementById("monthSelect")?.value || "";
        const year = document.getElementById("yearSelect")?.value || "";

        const today = new Date();
        const generatedDate =
            today.getDate().toString().padStart(2, "0") + "/" +
            (today.getMonth() + 1).toString().padStart(2, "0") + "/" +
            today.getFullYear();

        let y = 20;

        // ===== HEADER =====
        doc.setFont("helvetica", "bold");
        doc.setFontSize(26);
        doc.text("MoneyMitra", pageWidth / 2, y, { align: "center" });

        y += 12;

        doc.setFontSize(18);
        doc.text("Monthly Expense Report", pageWidth / 2, y, { align: "center" });

        y += 15;

        doc.setFont("helvetica", "normal");
        doc.setFontSize(14);

        doc.text(`Report Period: ${month} ${year}`, 20, y);
        doc.text(`Generated on: ${generatedDate}`, pageWidth - 20, y, { align: "right" });

        y += 5;
        doc.line(20, y, pageWidth - 20, y);

        y += 20;

        // ===== INCOME SUMMARY =====
        doc.setFont("helvetica", "bold");
        doc.setFontSize(18);
        doc.text("INCOME SUMMARY", 20, y);

        y += 15;
        doc.setFont("helvetica", "normal");
        doc.setFontSize(16);

        incomes.forEach(item => {
            doc.text(item.income_source, 20, y);
            doc.text(formatCurrency(item.amount), pageWidth - 20, y, { align: "right" });
            y += 12;
        });

        doc.setFont("helvetica", "bold");
        doc.text("Total Income", 20, y);
        doc.text(formatCurrency(totalIncome), pageWidth - 20, y, { align: "right" });

        y += 25;

        // ===== EXPENSE SUMMARY =====
        doc.setFontSize(18);
        doc.text("EXPENSE SUMMARY", 20, y);

        y += 15;
        doc.setFont("helvetica", "normal");
        doc.setFontSize(16);

        expenses.forEach(item => {
            doc.text(item.category, 20, y);
            doc.text(formatCurrency(item.expense_amount), pageWidth - 20, y, { align: "right" });
            y += 12;
        });

        doc.setFont("helvetica", "bold");
        doc.text("Net Balance", 20, y);
        doc.text(formatCurrency(balance), pageWidth - 20, y, { align: "right" });

        return doc.output("blob");
    }

    function downloadPDF() {
        const blob = generatePDFBlob();
        const link = document.createElement("a");
        link.href = URL.createObjectURL(blob);
        link.download = "Monthly_Expense_Report.pdf";
        document.body.appendChild(link);
        link.click();
        document.body.removeChild(link);
    }

    async function sharePDF() {

        const blob = generatePDFBlob();
        const file = new File([blob], "Monthly_Expense_Report.pdf", {
            type: "application/pdf"
        });

        if (navigator.canShare && navigator.canShare({ files: [file] })) {
            await navigator.share({
                title: "Monthly Expense Report",
                files: [file]
            });
        } else {
            downloadPDF();
            alert("Sharing not supported on this device.");
        }
    }

    downloadBtn.addEventListener("click", downloadPDF);
    shareBtn.addEventListener("click", sharePDF);

});