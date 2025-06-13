FROM quay.io/keycloak/keycloak:26.1.2

# Set environment variables for the database connection
ENV KC_DB=postgres
ENV KC_DB_URL=jdbc:postgresql://keycloak_postgres:5432/keycloak
ENV KC_DB_USERNAME=keycloak
ENV KC_DB_PASSWORD=password
ENV KC_HOSTNAME=localhost
ENV KEYCLOAK_OPTIMIZED=false
ENV KC_METRICS_ENABLED=true
ENV KC_HTTP_METRICS_HISTOGRAMS_ENABLED=true


# Copy the custom theme to Keycloak
RUN mkdir -p /opt/keycloak/themes/custom-theme
# Copy the custom theme into the Keycloak themes directory
COPY themes/custom-theme/custom.v2 /opt/keycloak/themes/custom-theme

# Copy the realm export file to the Keycloak import directory
COPY export_data_export /opt/keycloak/data/import

RUN mkdir -p /opt/keycloak/providers
# Copy the Custom Authenticator JAR
COPY target/custom-authenticator.jar /opt/keycloak/providers/

# Expose port 8080
EXPOSE 8080

# Command to start Keycloak and import the realm with OVERWRITE_EXISTING strategy
ENTRYPOINT ["/opt/keycloak/bin/kc.sh", "start-dev", "--import-realm"]


# --- Production-specific considerations ---
# 1. For production, avoid using "start-dev". Instead, use the default "start" command:
# ENTRYPOINT ["/opt/keycloak/bin/kc.sh", "start"]
# 2. Use environment variables for configuration management to avoid exposing sensitive data in the Dockerfile.
# 3. Implement logging and monitoring tools like Prometheus or ELK Stack for production readiness.