// REGISTER PAGE VALIDATION

document.addEventListener("DOMContentLoaded", function(){

    const form = document.querySelector("form");
    const emailInput = document.querySelector("input[name='email']");
    const passwordInput = document.querySelector("input[name='password']");
    const fullNameInput = document.querySelector("input[name='full_name']");

    form.addEventListener("submit", function(e){

        let valid = true;

        // Clear old error messages
        document.querySelectorAll(".error-msg").forEach(el => el.remove());

        // 🔹 Full Name Validation
        if(fullNameInput.value.trim().length < 3){
            showError(fullNameInput, "Full name must be at least 3 characters");
            valid = false;
        }

        // 🔹 Email Validation
        const emailPattern = /^[^ ]+@[^ ]+\.[a-z]{2,3}$/;
        if(!emailPattern.test(emailInput.value)){
            showError(emailInput, "Enter a valid email address");
            valid = false;
        }

        // 🔹 Password Validation
        if(passwordInput.value.length < 6){
            showError(passwordInput, "Password must be at least 6 characters");
            valid = false;
        }

        if(!valid){
            e.preventDefault(); // Stop form submit
        }

    });

    function showError(input, message){
        const error = document.createElement("div");
        error.classList.add("error-msg");
        error.style.color = "red";
        error.style.fontSize = "13px";
        error.style.marginTop = "5px";
        error.innerText = message;
        input.parentNode.appendChild(error);
    }

});