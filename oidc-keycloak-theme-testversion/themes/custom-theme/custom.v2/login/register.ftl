<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Register</title>
    <link rel="stylesheet" type="text/css" href="${url.resourcesPath}/css/style_register.css">
    <script>
        document.addEventListener('DOMContentLoaded', function() {
            const errorMessage = document.querySelector('.error-message');
            if (errorMessage) {
                setTimeout(function() {
                    errorMessage.classList.add('hidden');
                }, 6000);
            }

            document.getElementById('register-form').addEventListener('submit', function(event) {
                var username = document.getElementById('username').value;
                var email = document.getElementById('email').value;
                var password = document.getElementById('password').value;
                var confirmPassword = document.getElementById('password-confirm').value;
                var firstName = document.getElementById('firstName').value;
                var lastName = document.getElementById('lastName').value;
                var locale = document.getElementById('locale').value;
                var profile = document.getElementById('profile').value;
                var phone = document.getElementById('phone').value;
                var address = document.getElementById('address').value;

                if (!username || !email || !password || !confirmPassword || !firstName || !lastName || !locale || !profile || !phone || !address) {
                    event.preventDefault();
                    alert('Please fill in all fields.');
                } else if (password !== confirmPassword) {
                    event.preventDefault();
                    alert('Passwords do not match.');
                }
            });
        });
    </script>
</head>
<body>
    <div class="container">
        <div class="logo">
            <img src="${url.resourcesPath}/img/logo_cosiness.png" alt="Custom Logo">
        </div>
        <!-- Display error message if it exists -->
        <#if message?? && message?has_content>
            <span class="error-message" aria-live="assertive">
                ${message.getSummary()?no_esc}
            </span>
        </#if>
        <h1>Create an Account</h1>
        <form id="register-form" class="form-signin" action="${url.registrationAction}" method="post">
            <div class="form-group">
                <input type="text" id="username" name="username" class="form-control" placeholder="${msg('username')}" autofocus autocomplete="off" required />
            </div>
            <div class="form-group">
                <input type="email" id="email" name="email" class="form-control" placeholder="${msg('email')}" autocomplete="off" required />
            </div>
            <div class="form-group">
                <input type="password" id="password" name="password" class="form-control" placeholder="${msg('password')}" autocomplete="off" required />
            </div>
            <div class="form-group">
                <input type="password" id="password-confirm" name="password-confirm" class="form-control" placeholder="${msg('Confirm Password')}" required />
            </div>
            <div class="form-group">
                <input type="text" id="firstName" name="firstName" class="form-control" placeholder="${msg('First name')}" autocomplete="off" required />
            </div>
            <div class="form-group">
                <input type="text" id="lastName" name="lastName" class="form-control" placeholder="${msg('Last name')}" autocomplete="off" required />
            </div>
            <div class="form-group">
                <input type="text" id="locale" name="locale" class="form-control" placeholder="${msg('Locale')}" autocomplete="off" required />
            </div>
            <div class="form-group">
                <input type="text" id="profile" name="profile" class="form-control" placeholder="${msg('Profile')}" autocomplete="off" required />
            </div>
            <div class="form-group">
                <input type="text" id="phone" name="phone" class="form-control" placeholder="${msg('Phone Number')}" autocomplete="off" required />
            </div>
            <div class="form-group">
                <input type="text" id="address" name="address" class="form-control" placeholder="${msg('Address')}" autocomplete="off" required />
            </div>
            <div class="form-group">
                <button class="btn btn-lg btn-primary btn-block" type="submit">${msg('Register')}</button>
            </div>
            <div class="form-group">
                <span>${msg("alreadyHaveAccount")} <a href="${url.loginUrl}">${msg("Login")}</a></span>
            </div>
        </form>
    </div>
</body>
</html>
