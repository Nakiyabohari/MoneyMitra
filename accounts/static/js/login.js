document.addEventListener("DOMContentLoaded", function(){

    const loginBtn = document.getElementById("loginBtn");

    loginBtn.addEventListener("click", function(){

        const email = document.getElementById("email").value;
        const password = document.getElementById("password").value;

        if(!email || !password){
            alert("Please fill all fields");
            return;
        }

        // Temporary login logic (frontend only)
        localStorage.setItem("userEmail", email);

        window.location.href = "income.html";
    });

});