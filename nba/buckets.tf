# Create bucket to deploy code to
resource "google_storage_bucket" "deploy_bucket" {
  name = "function_deploy_hockey_nba_${var.gcp_project_id}"
  location      = "US"
  #force_destroy = true
}