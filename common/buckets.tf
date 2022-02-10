# Create bucket to deploy code to
resource "google_storage_bucket" "deploy_bucket_common" {
  name = "function_deploy_common_${var.gcp_project_id}"
  location      = "US"
  #force_destroy = true
}
