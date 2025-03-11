    function togglePassword() {
        let passwordInput = document.getElementById("password");
        let label = document.querySelector("label[onclick]");

        if (passwordInput.type === "password") {
            passwordInput.type = "text";
            label.textContent = "Hide";
        } else {
            passwordInput.type = "password";
            label.textContent = "Show";
        }
    }