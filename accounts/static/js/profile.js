// PROFILE PAGE SCRIPT

document.addEventListener("DOMContentLoaded", function () {

    // 🔹 Profile Image Preview
    const fileInput = document.querySelector("input[name='profile_photo']");
    const profileImage = document.querySelector(".profile-avatar img");

    if (fileInput) {
        fileInput.addEventListener("change", function () {

            const file = this.files[0];

            if (file) {
                const reader = new FileReader();

                reader.addEventListener("load", function () {
                    if (profileImage) {
                        profileImage.setAttribute("src", this.result);
                    }
                });

                reader.readAsDataURL(file);
            }
        });
    }

    // 🔹 Confirm Logout
    const logoutBtn = document.querySelector(".logout-button");

    if (logoutBtn) {
        logoutBtn.addEventListener("click", function (e) {
            const confirmLogout = confirm("Are you sure you want to logout?");
            if (!confirmLogout) {
                e.preventDefault();
            }
        });
    }

    // 🔹 Back Button
    const backBtn = document.querySelector(".back-button");

    if (backBtn) {
        backBtn.addEventListener("click", function () {
            window.history.back();
        });
    }

});