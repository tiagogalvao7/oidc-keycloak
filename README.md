Each directory have a README file with some informations and configurations about respective components.

To test our implementation, just follow the steps below.

## 1º [`oidc-risk-module-main`](./oidc-risk-module-main) and [`oidc-keycloak-theme-testversion`](./oidc-keycloak-theme-testversion)

### 1.1 Running the Complete System (Keycloak with Risk Module)
- ``git clone <oidc-risk-module-main>``
- ``git clone <oidc-keycloak-theme-testversion>``
- ``cd oidc-risk-module-main``
- Start the services with ``docker-compose up --build``
  
<ins>**Verification:**</ins>
- Open http://127.0.0.1:5001 in your browser to test the API, or test with Keycloak.
- Open http://127.0.0.1:8080 to access the Keycloak admin interface.
- Log in using admin credentials (default: username `admin`, password `admin`).
- Check the [`README`](./oidc-keycloak-theme-testversion#readme) to see more information about the screens.
- To stop and remove the volumes and the containers (optional): ``docker-compose down -v``

## 2º [`Flask-Client-Application`](./Flask-Client-Application)

- ``git clone <Flask-Client-Application>``
- ``cd Flask-Client-Application`` and run ``pip install -r requirements.txt`` to install all the necessary requirements, and run ``python FlaskClient.py`` to up the test application

<ins>**Verification:**</ins>
- Open http://127.0.0.1:5000 in your browser.
- Follow the [`README`](./Flask-Client-Application#readme) for detailed context and login images.
- If a dependency installation error appears, install the missing dependency manually.

## Notes for Production Deployment
For deploying to production, consider the following adjustments:

Each project has a Dockerfile and a docker-compose to run the projects individually.

1. **Environment Variables:** Use a ``.env`` file for managing environment-specific settings, such as database passwords or API URLs.
2. **Security:** Replace default passwords, and ensure sensitive information is secured.
3. **Production Optimizations:** Remove unnecessary development dependencies, improve logging, and configure your services for performance in production.
