output "resource_group" {
  value = azurerm_resource_group.main.name
}

output "acr_name" {
  value = azurerm_container_registry.main.name
}

output "container_app_name" {
  value = "ca-${local.name}"
}

output "app_url" {
  description = "Public URL of the app (available once deploy_app = true)."
  value       = var.deploy_app ? "https://${azurerm_container_app.web[0].ingress[0].fqdn}" : "not deployed yet"
}

output "github_variables" {
  description = "Values to add under GitHub > Settings > Secrets and variables > Actions > Variables."
  value       = {
    AZURE_CLIENT_ID       = azurerm_user_assigned_identity.github.client_id
    AZURE_TENANT_ID       = azurerm_user_assigned_identity.github.tenant_id
    AZURE_SUBSCRIPTION_ID = var.subscription_id
    ACR_NAME              = azurerm_container_registry.main.name
    RESOURCE_GROUP        = azurerm_resource_group.main.name
    CONTAINER_APP         = "ca-${local.name}"
  }
}
