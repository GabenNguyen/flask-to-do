function set_action_form(action) {
    let form = document.getElementById("auth-form");

    //Use of querySelector to select the first element with the class "btn-login"
    let login_btn = document.querySelector(".btn-login"); 

    //Use of querySelector to select the first element with the class "btn-sign_up"
    let sign_up_btn = document.querySelector(".btn-sign-up");

    if(action === "login") {
        // use of getAttribute dynamically set to the URL stored 
        // in the data_login_url attribute of the login_btn button.
        form.action = login_btn.getAttribute("data_login_url");
        form.method = "post"; // form method set to "post" as the form will be submitted
        form.submit(); // call the submit function to submit the form
        
    } else if(action === "sign_up") {
        // use of getAttribute to dynamically set to the URL stored 
        // in the data_login_url attribute of the sign_up_btn button.
        form.action = sign_up_btn.getAttribute("data_sign_up_url");
        form.method = "post";
        form.submit();
    }
}

function update_password_strength_bar() {
    let password_input = document.querySelector(".sign-up-input-password");
    let password_strength_bar = document.getElementById("password-strength-bar");
    let password_strength_text = document.getElementById("password-strength-text");

    password_input.addEventListener("input", function() {
        let password = password_input.value;

        // Criterias for password strength
        // Use const as the values are constant
        const has_uppercase = /[A-Z]/.test(password);
        const has_lowercase = /[a-z]/.test(password);
        const has_special_char = /[!@#$%^&*]/.test(password);
        const has_number = /[0-9]/.test(password);
        const is_long_enough = password.length >= 8;

        // Increase the strength by 1 for each criteria
        let strength = 0;
        if(has_uppercase) {
            strength++;
        }
        if(has_lowercase) {
            strength++;
        }
        if(has_special_char) {
            strength++;
        }
        if(has_number) {
            strength++;
        }
        if(is_long_enough) {
            strength++;
        }
        
        // Convert into percentage and update the bar width
        let bar_width = (strength / 5) * 100;
        password_strength_bar.style.width = bar_width + "%";

        //Update the password strength text and password strength bar
        if(strength === 0) {
            password_strength_bar.style.backgroundColor = "white";
            password_strength_text.style.color = "white";
            password_strength_text.textContent = "";
        } else if(strength === 1) {
            password_strength_bar.style.backgroundColor = "red";
            password_strength_text.style.color = "red";
            password_strength_text.textContent = "Weak";
        } else if(strength === 2) {
            password_strength_bar.style.backgroundColor = "orange";
            password_strength_text.style.color = "orange";
            password_strength_text.textContent = "Medium";
        } else if(strength === 3 || strength === 4) {
            password_strength_bar.style.backgroundColor = "darkyellow";
            password_strength_text.style.color = "darkyellow";
            password_strength_text.textContent = "Decent";
        } else if(strength == 5) {
            password_strength_bar.style.backgroundColor = "green";
            password_strength_text.style.color = "green";
            password_strength_text.textContent = "Strong";
        }
    });
}

update_password_strength_bar();