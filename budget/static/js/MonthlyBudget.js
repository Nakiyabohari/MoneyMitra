document.addEventListener("DOMContentLoaded", function () {

    const categorySelect = document.getElementById("categorySelect");
    const customField = document.getElementById("customCategoryField");

    // Hide custom field initially
    customField.style.display = "none";

    categorySelect.addEventListener("change", function () {

        if (categorySelect.value === "Custom") {
            customField.style.display = "block";
        }
        else {
            customField.style.display = "none";
        }

    });

});