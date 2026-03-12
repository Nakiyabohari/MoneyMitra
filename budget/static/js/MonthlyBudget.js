document.addEventListener("DOMContentLoaded", function () {

    const categorySelect = document.getElementById("categorySelect");
    const customField = document.getElementById("customCategoryField");

    if (categorySelect) {

        customField.style.display = "none";

        categorySelect.addEventListener("change", function () {

            if (categorySelect.value === "Custom") {
                customField.style.display = "block";
            } else {
                customField.style.display = "none";
            }

        });

    }

});


/* ================================
   DELETE BUDGET
================================ */

function deleteBudget(id){

    if(confirm("Delete this budget?")){

        fetch(`/budget/delete_budget/${id}/`, {

            method: "POST",

            headers: {
                "X-CSRFToken": getCookie("csrftoken"),
                "Content-Type": "application/json"
            }

        })

        .then(response => response.json())

        .then(data => {

            if(data.success){

                location.reload();

            }else{

                alert("Delete failed");

            }

        })

        .catch(error => {

            console.error("Error:", error);

        });

    }

}



/* ================================
   SHOW EDIT BOX
================================ */

function toggleEdit(id){

    const box = document.getElementById("editBox"+id);

    if(box.style.display === "none"){

        box.style.display = "block";

    }else{

        box.style.display = "none";

    }

}



/* ================================
   SAVE EDIT
================================ */

function saveEdit(id){

    const amount = document.getElementById("editAmount"+id).value;

    fetch(`/budget/edit_budget/${id}/`, {

        method: "POST",

        headers: {
            "X-CSRFToken": getCookie("csrftoken"),
            "Content-Type": "application/json"
        },

        body: JSON.stringify({
            amount: amount
        })

    })

    .then(response => response.json())

    .then(data => {

        if(data.success){

            location.reload();

        }else{

            alert("Update failed");

        }

    })

    .catch(error => {

        console.error("Error:", error);

    });

}



/* ================================
   CSRF TOKEN FUNCTION
================================ */

function getCookie(name) {

    let cookieValue = null;

    if (document.cookie && document.cookie !== '') {

        const cookies = document.cookie.split(';');

        for (let i = 0; i < cookies.length; i++) {

            const cookie = cookies[i].trim();

            if (cookie.substring(0, name.length + 1) === (name + '=')) {

                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));

                break;

            }

        }

    }

    return cookieValue;

}