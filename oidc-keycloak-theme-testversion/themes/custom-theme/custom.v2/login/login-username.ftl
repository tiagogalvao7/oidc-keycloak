<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Login</title>
    <link rel="stylesheet" type="text/css" href="${url.resourcesPath}/css/login-username.css">
</head>
<body>
    <div class="container">
        <div class="logo">
            <img src="${url.resourcesPath}/img/logo.png" alt="Custom Logo">
        </div>

        <h1>Login</h1>

        <form id="kc-username-login-form" class="form-signin" action="${url.loginAction}" method="post">
            <input type="hidden" id="url-login-action" value="${url.loginAction}">

            <div class="form-group">
                <input type="text" id="username" name="username" class="form-control"
                       placeholder="<#if !realm.loginWithEmailAllowed>${msg("username")}<#elseif !realm.registrationEmailAsUsername>${msg("usernameOrEmail")}<#else>${msg("email")}</#if>"
                       value="${login.username!''}" autofocus autocomplete="off"
                       aria-invalid="<#if messagesPerField.existsError('username')>true</#if>"/>
                <#if messagesPerField.existsError('username')>
                    <span class="error-message" aria-live="assertive">
                        ${kcSanitize(messagesPerField.get('username'))?no_esc}
                    </span>
                </#if>
            </div>

            <div class="form-group">
                <button class="btn btn-primary btn-block" type="submit">${msg("doLogIn")}</button>
            </div>

            <div class="form-options-wrapper">
                <#if realm.resetPasswordAllowed>
                    <span><a tabindex="5" href="${url.loginResetCredentialsUrl}">${msg("doForgotPassword")}</a></span>
                </#if>
            </div>
        </form>

        <#if realm.password && realm.registrationAllowed && !registrationDisabled??>
            <div id="kc-registration-container">
                <div id="kc-registration">
                    <span>${msg("noAccount")} <a tabindex="6" href="${url.registrationUrl}">${msg("doRegister")}</a></span>
                </div>
            </div>
        </#if>
        <div class="container::after"></div>
    </div>
</body>
</html>