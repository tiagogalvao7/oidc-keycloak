<#import "template.ftl" as layout>
<#import "password-commons.ftl" as passwordCommons>

<@layout.registrationLayout displayRequiredFields=false displayMessage=!messagesPerField.existsError('totp','userLabel'); section>
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Configure Two-Factor Authentication</title>
        <link rel="stylesheet" type="text/css" href="${url.resourcesPath}/css/totp.css">
    </head>
    <#if section = "header">
        Configure Two-Factor Authentication
    <#elseif section = "form">
        <ol id="kc-totp-settings">
            <li>
                <p>1. Scan the QR code with your authenticator app (e.g., Google Authenticator, Authy).</p>
                <ul id="kc-totp-supported-apps">
                    <li>Google Authenticator</li>
                    <li>Authy</li>
                    <li>Microsoft Authenticator</li>
                </ul>
            </li>
            <#if mode?? && mode = "manual">
                <li>
                    <p>Or enter this secret key manually into your app:</p>
                    <p><span id="kc-totp-secret-key">${totp.totpSecretEncoded}</span></p>
                    <p><a href="${totp.qrUrl}" id="mode-barcode">Rescan QR code</a></p>
                </li>
                <li>
                    <p>Configuration details:</p>
                    <p>
                    <ul>
                        <li id="kc-totp-type">Type: ${msg("loginTotp." + totp.policy.type)}</li>
                        <li id="kc-totp-algorithm">Algorithm: ${totp.policy.getAlgorithmKey()}</li>
                        <li id="kc-totp-digits">Digits: ${totp.policy.digits}</li>
                        <#if totp.policy.type = "totp">
                            <li id="kc-totp-period">Interval: ${totp.policy.period} seconds</li>
                        <#elseif totp.policy.type = "hotp">
                            <li id="kc-totp-counter">Initial Counter: ${totp.policy.initialCounter}</li>
                        </#if>
                    </ul>
                    </p>
                </li>
            <#else>
                <li>
                    <p>2. Scan this QR code in your application:</p>
                    <img id="kc-totp-secret-qr-code" src="data:image/png;base64, ${totp.totpSecretQrCode}" alt="QR Code"><br/>
                    <p><a href="${totp.manualUrl}" id="mode-manual">Cannot scan the code? Enter the key manually.</a></p>
                </li>
            </#if>
            <li>
                <p>3. Enter the security code generated by the app and a name for this device.</p>
            </li>
        </ol>

        <form action="${url.loginAction}" class="${properties.kcFormClass!}" id="kc-totp-settings-form" method="post">
            <div class="${properties.kcFormGroupClass!}">
                <div class="${properties.kcInputWrapperClass!}">
                    <label for="totp" class="control-label">Security Code <span class="required">*</span></label>
                </div>
                <div class="${properties.kcInputWrapperClass!}">
                    <input type="text" id="totp" name="totp" autocomplete="off" class="${properties.kcInputClass!}"
                           aria-invalid="<#if messagesPerField.existsError('totp')>true</#if>"
                    />
                    <#if messagesPerField.existsError('totp')>
                        <span id="input-error-otp-code" class="${properties.kcInputErrorMessageClass!}" aria-live="polite">
                            ${kcSanitize(messagesPerField.get('totp'))?no_esc}
                        </span>
                    </#if>
                </div>
                <input type="hidden" id="totpSecret" name="totpSecret" value="${totp.totpSecret}" />
                <#if mode??><input type="hidden" id="mode" name="mode" value="${mode}"/></#if>
            </div>

            <div class="${properties.kcFormGroupClass!}">
                <div class="${properties.kcInputWrapperClass!}">
                    <label for="userLabel" class="control-label">Device Name <#if totp.otpCredentials?size gte 1><span class="required">*</span></#if></label>
                </div>
                <div class="${properties.kcInputWrapperClass!}">
                    <input type="text" class="${properties.kcInputClass!}" id="userLabel" name="userLabel" autocomplete="off"
                           aria-invalid="<#if messagesPerField.existsError('userLabel')>true</#if>"
                    />
                    <#if messagesPerField.existsError('userLabel')>
                        <span id="input-error-otp-label" class="${properties.kcInputErrorMessageClass!}" aria-live="polite">
                            ${kcSanitize(messagesPerField.get('userLabel'))?no_esc}
                        </span>
                    </#if>
                </div>
            </div>

            <div class="${properties.kcFormGroupClass!}">
                <@passwordCommons.logoutOtherSessions/>
            </div>

            <#if isAppInitiatedAction??>
                <input type="submit"
                       class="pf-c-button pf-m-primary pf-m-block btn-lg"
                       id="saveTOTPBtn" value="Save"
                />
                <button type="submit"
                        class="pf-c-button pf-m-secondary pf-m-block btn-lg"
                        id="cancelTOTPBtn" name="cancel-aia" value="true" />Cancel
                </button>
            <#else>
                <input type="submit"
                       class="pf-c-button pf-m-primary pf-m-block btn-lg"
                       id="saveTOTPBtn" value="Save"
                />
            </#if>
        </form>
    </#if>
</@layout.registrationLayout>