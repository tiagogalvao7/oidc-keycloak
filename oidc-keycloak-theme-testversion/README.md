# oidc-keycloack-theme-testsversion

OIDC-PRINCE theme for Keycloak Login

In this project the claims are generated and sent randomly by the login.ftl file so that you can see a greater diversity of results on the screens where the API calculation values are received (Login screen with GDPR Compliance, and the Grant Access screen with the risk associated with each claim), together with the Flask-Client-Application, you can test the entire implementation.

## Steps do test and use OIDC Login Keycloak theme

All the Keycloak settings are have been configured beforehand, and all you have to do is run docker to enter the Keycloak interface and see the whole process.

## Some Keycloak Configurations

### Create Clients
![Create Clients](docs/Keycloak_createclient.png)

### Create Users
![Create userst](docs/Keycloak_createuser.png)

### Create Client Scopes, to trigger client authentications flows
![Client Scopes](docs/Keycloak_createclientscopes.png)

### Authentications Flows
![Authentication Flows](docs/Keycloak_flow.png)
![Authentication Flows](docs/Keycloak_flow1.png)

**Explanation of how the screens interact**: three screens were developed for our theme: Login screen, Create user screen and Grant Access screen.

## Login Page Theme

![OIDC-PRINCE login theme for Keycloak](docs/themeLogin.png)

## Sign Up Page Theme

![OIDC-PRINCE login theme for Keycloak](docs/themeRegister.png)

## Grant Access Page Theme

![OIDC-PRINCE login theme for Keycloak](docs/themeGrant1.png)
![OIDC-PRINCE login theme for Keycloak](docs/themeGrant2.png)

To allow you to preview the screens, three .html files are provided so that you can see how the themes look without having to use Keycloak.
