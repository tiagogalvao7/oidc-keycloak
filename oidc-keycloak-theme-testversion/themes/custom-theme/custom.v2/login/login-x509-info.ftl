<#import "template.ftl" as layout>
<@layout.registrationLayout; section>
  <#if section = "header">
    ${msg("doLogIn")}
  <#elseif section = "form">
    <link rel="stylesheet" href="${url.resourcesPath}/css/x509.css">
    <div class="login-container">
      <h1>${msg("doLogIn")}</h1>
      <div>
        <label for="certificate_subjectDN">${msg("clientCertificate")}</label>
        <#if x509.formData.subjectDN??>
          <div>${(x509.formData.subjectDN!"")}</div>
        <#else>
          <div>${msg("noCertificate")}</div>
        </#if>
      </div>

      <#if x509.formData.isUserEnabled??>
        <div>
          <label for="username">${msg("doX509LoginAs")}</label>
          <div>${(x509.formData.username!'')}</div>
        </div>
      </#if>

      <form action="${url.loginAction}" method="post">
        <div class="button-container">
          <button class="primary" type="submit" name="action" value="continue">${msg("doContinue")}</button>
          <button class="default" type="submit" name="action" value="ignore">${msg("doIgnore")}</button>
        </div>
      </form>
    </div>
  </#if>
</@layout.registrationLayout>
