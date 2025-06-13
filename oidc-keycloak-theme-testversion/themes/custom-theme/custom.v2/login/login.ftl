<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Login</title>
    <link rel="stylesheet" type="text/css" href="${url.resourcesPath}/css/style.css">
    <script>
        document.addEventListener('DOMContentLoaded', function() {
            console.log("DOM fully loaded and parsed.");

            // Hide the error message after 5 seconds
            const errorMessage = document.querySelector('.error-message');
            if (errorMessage) {
                setTimeout(function() {
                    errorMessage.classList.add('hidden');
                }, 5000);
            }

            // Predefined list of claims
            const claimsList = [
                "sub",
                "name",
                "email",
                "birthdate",
                "gender",
                "phone_number",
                "address",
                "locale",
                "preferred_username",
                "picture"
            ];

            // Function to randomly select a subset of claims
            function getRandomClaims(claims, number) {
                let shuffled = claims.sort(() => 0.5 - Math.random());
                return shuffled.slice(0, number);
            }

            // Select a random subset of up to 5 claims
            const selectedClaims = getRandomClaims(claimsList, 5);
            const claimsString = selectedClaims.join(',');
            console.log('Randomly selected claims:', claimsString);

            // Fetch GDPR compliance percentage from the API using the selected random claims
            fetch('http://127.0.0.1:5001/compliance/osp?claims=' + encodeURIComponent(claimsString))
                .then(response => response.json())
                .then(data => {
                    console.log('Processed data:', data);
                    const compliancePercentage = data.compliance_percentage;
                    document.getElementById('compliance-percentage').textContent = compliancePercentage + '%';

                    // Change the color of the triangle based on compliance percentage
                    const triangleElement = document.querySelector('.triangle');
                    triangleElement.classList.remove('low', 'medium', 'high');
                    if (compliancePercentage < 50) {
                        triangleElement.classList.add('low');
                    } else if (compliancePercentage < 70) {
                        triangleElement.classList.add('medium');
                    } else {
                        triangleElement.classList.add('high');
                    }
                })
                .catch(error => {
                    console.error('Error fetching compliance percentage:', error);
                    document.getElementById('compliance-percentage').textContent = 'N/A';
                });

            // Login form validation
            document.getElementById('kc-form-login').addEventListener('submit', function(event) {
                var username = document.getElementById('username').value;
                var password = document.getElementById('password').value;
                console.log('Login attempt with user:', username);
                if (!username || !password) {
                    event.preventDefault();
                    alert('Please fill in all fields.');
                }
            });

            // Toggle GDPR info popup
            document.querySelector('.info-button-gdpr').addEventListener('click', function(event) {
                event.stopPropagation();
                const popup = document.getElementById('infoPopupGDPR');
                popup.style.display = popup.style.display === 'block' ? 'none' : 'block';
            });

            // Close popup when clicking outside
            document.addEventListener('click', function(event) {
                const popup = document.getElementById('infoPopupGDPR');
                if (popup.style.display === 'block' && !popup.contains(event.target) && !event.target.matches('.info-button-gdpr')) {
                    popup.style.display = 'none';
                }
            });
        });
    </script>
</head>
<body>
    <div class="container">
        <div class="logo">
            <img src="${url.resourcesPath}/img/logo.png" alt="Custom Logo">
        </div>
        <div id="api-value" class="api-value-container">
            <div class="info-wrapper">
                <div class="triangle">
                    <div class="exclamation">!</div>
                </div>
                <div class="info-text-container">
                    <span class="info-text">Service A is <span id="compliance-percentage">x%</span> compliant with GDPR</span>
                    <button class="info-button-gdpr">i</button>
                    <div class="info-popup" id="infoPopupGDPR">
                        <p>GDPR (General Data Protection Regulation) is a regulation in EU law on data protection and privacy for all individuals within the European Union.</p>
                    </div>
                    <span class="info-note">(proceed with caution)</span>
                </div>
            </div>
        </div>
        <h1>Login</h1>
        <form id="kc-form-login" class="form-signin" onsubmit="login.disabled = true; return true;" action="${url.loginAction}" method="post">
            <input type="hidden" id="url-login-action" value="${url.loginAction}">
            <input type="hidden" id="msg-username" value="${msg('username')}">
            <input type="hidden" id="msg-password" value="${msg('password')}">
            <input type="hidden" id="msg-do-log-in" value="${msg('doLogIn')}">

            <#if !usernameHidden??>
                <div class="form-group">
                    <input type="text" id="username" name="username" class="form-control" placeholder="${msg('username')}" value="${(login.username!'')}" autofocus autocomplete="off"
                           aria-invalid="<#if messagesPerField.existsError('username','password')>true</#if>"
                    />
                    <#if messagesPerField.existsError('username','password')>
                        <span class="error-message" aria-live="assertive">
                            ${kcSanitize(messagesPerField.getFirstError('username','password'))?no_esc}
                        </span>
                    </#if>
                </div>
            </#if>
            <div class="form-group">
                <input type="password" id="password" name="password" class="form-control" placeholder="${msg('password')}" autocomplete="off"
                       aria-invalid="<#if messagesPerField.existsError('username','password')>true</#if>"
                />
                <#if usernameHidden?? && messagesPerField.existsError('username','password')>
                    <span class="error-message" aria-live="assertive">
                        ${kcSanitize(messagesPerField.getFirstError('username','password'))?no_esc}
                    </span>
                </#if>
            </div>
            <div class="form-group remember-forgot">
                <#if realm.rememberMe && !usernameHidden??>
                    <div class="checkbox">
                        <label>
                            <#if login.rememberMe??>
                                <input tabindex="3" id="rememberMe" name="rememberMe" type="checkbox" checked> ${msg("rememberMe")}
                            <#else>
                                <input tabindex="3" id="rememberMe" name="rememberMe" type="checkbox"> ${msg("rememberMe")}
                            </#if>
                        </label>
                    </div>
                </#if>
                <div class="form-options-wrapper">
                    <#if realm.resetPasswordAllowed>
                        <span><a tabindex="5" href="${url.loginResetCredentialsUrl}">${msg("doForgotPassword")}</a></span>
                    </#if>
                </div>
            </div>
            <div class="form-group">
                <button class="btn btn-lg btn-primary btn-block" type="submit">${msg('doLogIn')}</button>
            </div>
            <input type="hidden" id="id-hidden-input" name="credentialId" <#if auth.selectedCredential?has_content>value="${auth.selectedCredential}"</#if>/>

        </form>
        <#if realm.password && realm.registrationAllowed && !registrationDisabled??>
            <div id="kc-registration-container">
                <div id="kc-registration">
                    <span>${msg("noAccount")} <a tabindex="6" href="${url.registrationUrl}">${msg("doRegister")}</a></span>
                </div>
            </div>
        </#if>
        <#if realm.password && social.providers??>
            <div id="kc-social-providers" class="${properties.kcFormSocialAccountSectionClass!}">
                <hr/>
                <h4>${msg("identity-provider-login-label")}</h4>
                <ul class="${properties.kcFormSocialAccountListClass!} <#if social.providers?size gt 3>${properties.kcFormSocialAccountListGridClass!}</#if>">
                    <#list social.providers as p>
                        <li>
                            <a id="social-${p.alias}" class="${properties.kcFormSocialAccountListButtonClass!} <#if social.providers?size gt 3>${properties.kcFormSocialAccountGridItem!}</#if>"
                               type="button" href="${p.loginUrl}">
                                <#if p.iconClasses?has_content>
                                    <i class="${properties.kcCommonLogoIdP!} ${p.iconClasses!}" aria-hidden="true"></i>
                                    <span class="${properties.kcFormSocialAccountNameClass!} kc-social-icon-text">${p.displayName!}</span>
                                <#else>
                                    <span class="${properties.kcFormSocialAccountNameClass!}">${p.displayName!}</span>
                                </#if>
                            </a>
                        </li>
                    </#list>
                </ul>
            </div>
        </#if>
    </div>
</body>
</html>

