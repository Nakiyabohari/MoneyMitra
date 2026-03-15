document.addEventListener("DOMContentLoaded", function(){

    const emailInput = document.getElementById("email");
    const passwordInput = document.getElementById("password");
    const form = document.getElementById("loginForm");

    /* Autofill saved email */

    const savedEmail = localStorage.getItem("savedEmail");

    if(savedEmail){
        emailInput.value = savedEmail;
    }

    /* Form validation + save email */

    form.addEventListener("submit", function(e){

        const email = emailInput.value.trim();
        const password = passwordInput.value.trim();

        if(!email || !password){
            e.preventDefault();
            alert("Please fill all fields");
            return;
        }

        /* Save email for next login */

        localStorage.setItem("savedEmail", email);

    });

});