resource "google_service_account" "sa_sports_analytics" {
  account_id   = "sa-sports-analytics-api"
  display_name = "Service Account for Sports Analytics API to call backend resources"
}

resource "google_service_account_iam_member" "iam_sa_sports_analytics_function_invoker" {
  service_account_id = google_service_account.sa_sports_analytics.name
  role               = "roles/cloudfunctions.invoker"
  #member             = "serviceAccount:${google_service_account.sa_sports_analytics.email}"
}