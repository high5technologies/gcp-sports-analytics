resource "google_project_service" "project_apigateway" {
  project = var.gcp_project_id
  #service = "iam.googleapis.com"
  service = "apigateway.googleapis.com"
  disable_on_destroy = false
}

resource "google_project_service" "project_servicemanagement" {
  project = var.gcp_project_id
  service = "servicemanagement.googleapis.com"
  disable_on_destroy = false
}

resource "google_project_service" "project_servicecontrol" {
  project = var.gcp_project_id
  service = "servicecontrol.googleapis.com"
  disable_on_destroy = false
}

resource "google_project_service" "project_apikeys" {
  project = var.gcp_project_id
  service = "apikeys.googleapis.com"
  disable_on_destroy = false
}
