document.addEventListener("DOMContentLoaded", function () {

    // =============================
    // CATEGORY LOGIC
    // =============================
    const select = document.getElementById("categoryField");
    const input = document.getElementById("categoryInput");

    if (select && input) {

        select.addEventListener("change", function () {

            if (this.value === "custom") {
                select.classList.add("hidden");
                input.classList.remove("hidden");
                input.focus();
            }

        });

        // Add custom category on Enter
        input.addEventListener("keydown", function (event) {

            if (event.key === "Enter") {

                event.preventDefault();

                const value = input.value.trim();
                if (!value) return;

                // Remove previous custom option
                const existing = document.getElementById("dynamicCustomOption");
                if (existing) existing.remove();

                // Create new option
                const newOption = document.createElement("option");
                newOption.value = value;
                newOption.text = value;
                newOption.id = "dynamicCustomOption";
                newOption.selected = true;

                select.appendChild(newOption);

                input.value = "";
                input.classList.add("hidden");
                select.classList.remove("hidden");
            }

        });
    }

    // =============================
    // DATE FIELD
    // =============================
    const dateField = document.getElementById("expenseDate");

    if (dateField) {
        const today = new Date().toISOString().split("T")[0];
        dateField.max = today;
        dateField.value = today;
    }

    // =============================
    // 🔥 POPUP MESSAGE SYSTEM
    // =============================
    const messages = document.querySelectorAll("[class^='message-']");

    messages.forEach(msg => {

        const popup = document.createElement("div");
        popup.innerText = msg.innerText;

        popup.style.position = "fixed";
        popup.style.top = "20px";
        popup.style.right = "20px";
        popup.style.padding = "12px 18px";
        popup.style.borderRadius = "8px";
        popup.style.color = "#fff";
        popup.style.fontWeight = "500";
        popup.style.zIndex = "9999";
        popup.style.boxShadow = "0 4px 10px rgba(0,0,0,0.2)";
        popup.style.opacity = "0";
        popup.style.transform = "translateY(-10px)";
        popup.style.transition = "all 0.3s ease";

        // Color logic
        if (msg.classList.contains("message-error")) {
            popup.style.background = "#e53935"; // red
        } else {
            popup.style.background = "#43a047"; // green
        }

        document.body.appendChild(popup);

        // Animation in
        setTimeout(() => {
            popup.style.opacity = "1";
            popup.style.transform = "translateY(0)";
        }, 100);

        // Remove after 3 sec
        setTimeout(() => {
            popup.style.opacity = "0";
            popup.style.transform = "translateY(-10px)";
            setTimeout(() => popup.remove(), 300);
        }, 3000);

        // Hide original message
        msg.style.display = "none";
    });

    
});