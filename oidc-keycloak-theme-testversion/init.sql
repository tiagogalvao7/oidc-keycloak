-- Permitir acesso a estatísticas e vistas necessárias ao postgres_exporter
GRANT CONNECT ON DATABASE keycloak TO keycloak;
GRANT USAGE ON SCHEMA public TO keycloak;

GRANT SELECT ON pg_stat_database TO keycloak;
GRANT SELECT ON pg_stat_activity TO keycloak;
GRANT SELECT ON pg_stat_bgwriter TO keycloak;
GRANT SELECT ON pg_stat_user_tables TO keycloak;
GRANT SELECT ON pg_stat_user_indexes TO keycloak;
GRANT SELECT ON pg_statio_user_tables TO keycloak;
GRANT SELECT ON pg_statio_user_indexes TO keycloak;
GRANT SELECT ON pg_locks TO keycloak;

-- Extensão opcional, útil para estatísticas detalhadas
CREATE EXTENSION IF NOT EXISTS pg_stat_statements;
