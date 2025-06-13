// Policy JavaScript para Keycloak

// A função evaluate recebe o contexto da política e decide se a autorização é concedida ou negada
exports = function (context) {
  // Log para debugging
  console.log("Executing custom JS policy");

  // Obter informações do usuário autenticado
  var identity = context.identity;
  var attributes = identity.attributes;

  // Exemplo: negar acesso se o usuário não tiver um e-mail verificado
  if (attributes.email_verified !== "true") {
    console.log("Access denied: email not verified");
    context.deny();
    return;
  }

  // Exemplo: permitir acesso se o usuário for de um grupo específico
  var groups = identity.getGroups();
  if (groups.includes("admin") || groups.includes("manager")) {
    console.log("Access granted: user is in admin/manager group");
    context.grant();
    return;
  }

  // Exemplo: permitir acesso apenas em determinados horários
  var currentHour = new Date().getHours();
  if (currentHour < 8 || currentHour > 18) {
    console.log("Access denied: outside working hours");
    context.deny();
    return;
  }

  // Se nenhuma regra negar, conceder acesso
  console.log("Access granted by default");
  context.grant();
};
