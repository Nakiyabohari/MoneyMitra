document.addEventListener("DOMContentLoaded", function(){

    const loginBtn = document.getElementById("loginBtn");

    loginBtn.addEventListener("click", function(e){

        const email = document.getElementById("email").value;
        const password = document.getElementById("password").value;

        if(!email || !password){
            e.preventDefault();
            alert("Please fill all fields");
            return;
        }
    });

});