resource "google_service_account" "sa_sports_analytics" {
  account_id   = "sa-sports-analytics-api"
  display_name = "Service Account for Sports Analytics API to call backend resources"
}
resource "google_project_iam_member" "iam_sa_sports_analytics_function_invoker" {
  project = var.gcp_project_id
  role    = "roles/cloudfunctions.invoker"
  member = "serviceAccount:${google_service_account.sa_sports_analytics.email}"
}
resource "google_project_iam_member" "iam_sa_sports_analytics_cloudrun_invoker" {
  project = var.gcp_project_id
  role    = "roles/run.invoker"
  member = "serviceAccount:${google_service_account.sa_sports_analytics.email}"
}

#resource "google_service_account_iam_member" "iam_sa_sports_analytics_function_invoker" {
#  #service_account_id = google_service_account.sa_sports_analytics.name
#  role               = "roles/cloudfunctions.invoker"
#  member             = "serviceAccount:${google_service_account.sa_sports_analytics.email}"
#}
#resource "google_service_account" "sa-name" {
#  account_id = "sa-name"
#  display_name = "SA"
#}
#
#resource "google_project_iam_member" "firestore_owner_binding" {
#  project = <your_gcp_project_id_here>
#  role    = "roles/datastore.owner"
#  member  = "serviceAccount:${google_service_account.sa-name.email}"
#}