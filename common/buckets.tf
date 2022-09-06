# Create bucket to deploy code to
resource "google_storage_bucket" "deploy_bucket" {
  name = "function_deploy_common_${var.gcp_project_id}"
  location      = "US"
  #force_destroy = true
}

resource "google_storage_bucket" "reverse_etl_export_bucket" {
  name = "reverse_etl_export_${var.gcp_project_id}"
  location      = "US"
  #force_destroy = true
}

