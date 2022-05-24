locals {
  api_config_id_prefix     = "api"
  api_id                   = "sports-analytics-api"
  gateway_id               = "sports-analytics"
  display_name             = "API for Sports Analytics Consjmption"
}

resource "google_api_gateway_api" "api_gw" {
  provider     = google-beta
  #api_id       = local.api_gateway_container_id
  api_id       = local.api_id
  project      = var.gcp_project_id
  display_name = local.display_name

  depends_on = [google_project_service.project_apigateway,google_project_service.project_servicemanagement,google_project_service.project_servicecontrol]
}

