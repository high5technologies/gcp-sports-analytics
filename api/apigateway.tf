locals {
  api_config_id_prefix     = "api"
  api_id                   = "sports-analytics-api"
  gateway_id               = "sports-analytics"
  display_name             = "Sports Analytics API"
}

resource "google_api_gateway_api" "api_sports_analytics" {
  provider     = google-beta
  #api_id       = local.api_gateway_container_id
  api_id       = local.api_id
  project      = var.gcp_project_id
  display_name = local.display_name
  #managed_service = "${local.api_id}.apigateway.${var.gcp_project_id}.cloud.goog"
  depends_on = [google_project_service.project_apigateway,google_project_service.project_servicemanagement,google_project_service.project_servicecontrol]
}

resource "google_apikeys_key" "api_key_sports_analytics_app" {
  name         = "sports-analytics-app"
  display_name = "Sports Analytics - App"
  project      = var.gcp_project_id

  restrictions {
    api_targets {
      service = google_api_gateway_api.api_sports_analytics.managed_service
      #methods = ["GET*"]
    }

    #browser_key_restrictions {
    #  allowed_referrers = [".*"]
    #}
  }
  depends_on = [google_project_service.project_apikeys]
}

resource "google_apikeys_key" "api_key_sports_analytics_test" {
  name         = "sports-analytics-test"
  display_name = "Sports Analytics - Test"
  project      = var.gcp_project_id
  restrictions {
    api_targets {
      service = google_api_gateway_api.api_sports_analytics.managed_service
      #methods = ["GET*"]
    }
  }
  depends_on = [google_project_service.project_apikeys]
}

data "template_file" "openapi_file" {
  #template = file("${path.module}/userdata.sh")
  template = file("openapi_template.yml")
  
  vars = {
    MANAGED_SERVICE    = google_api_gateway_api.api_sports_analytics.managed_service
    GCP_REGION         = var.gcp_region
    GCP_PROJECT_ID     = var.gcp_project_id
  }
}

resource "google_api_gateway_api_config" "api_sports_analytics_config" {
  provider             = google-beta
  api                  = google_api_gateway_api.api_sports_analytics.api_id
  api_config_id_prefix = local.api_config_id_prefix
  project              = var.gcp_project_id
  display_name         = local.display_name

  openapi_documents {
    document {
      path     = "openapi.yml"
      #contents = filebase64("openapi.yml")
      #contents = data.template_file.openapi_file.rendered
      #contents = textencodebase64(data.template_file.openapi_file.rendered, "UTF-16LE")
      contents = base64encode(data.template_file.openapi_file.rendered)
    }
  }
  lifecycle {
    create_before_destroy = true
  }
  gateway_config {
    backend_config {
        google_service_account = google_service_account.sa_sports_analytics.email
    }
  }
  depends_on = [google_api_gateway_api.api_sports_analytics,google_apikeys_key.api_key_sports_analytics_app, google_apikeys_key.api_key_sports_analytics_test]
}

resource "google_api_gateway_gateway" "api_sports_analytics_gateway" {
  provider = google-beta
  region   = var.gcp_region
  project  = var.gcp_project_id
  api_config   = google_api_gateway_api_config.api_sports_analytics_config.id
  gateway_id   = local.gateway_id
  display_name = local.display_name

  #depends_on   = [google_api_gateway_api_config.api_sports_analytics_config, google_project_service.project_sports_analytics_api]
  depends_on   = [google_api_gateway_api_config.api_sports_analytics_config]
}

