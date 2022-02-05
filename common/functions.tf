module "function_SportsAnalytics_Common_Log_Error" {
  source = "../modules/function"

  project_name = var.gcp_project_id
  function_name = "SportsAnalytics_Common_Log_Error"
  function_description = "Log Errors to Firestore that come into the error log topic"
  function_deployment_bucket_name = google_storage_bucket.deploy_bucket.name
  function_entry_point = "common_error_log"
  function_region = var.gcp_region
  function_runtime = "python39"
  function_available_memory_mb = 128
  #function_trigger_http = null
  #function_event_trigger_type = "google.pubsub.topic.publish"
  function_event_trigger_resource = google_pubsub_topic.error_log_topic.name
}

module "function_SportsAnalytics_Common_BigQuery_Replication" {
  source = "../modules/function"

  project_name = var.gcp_project_id
  function_name = "SportsAnalytics_Common_BigQuery_Replication"
  function_description = "Replication pubsub message to BigQuery"
  function_deployment_bucket_name = google_storage_bucket.deploy_bucket.name
  function_entry_point = "pubsub_to_bigquery_replication"
  function_region = var.gcp_region
  function_runtime = "python39"
  function_available_memory_mb = 128
  #function_trigger_http = null
  #function_event_trigger_type = "google.pubsub.topic.publish"
  function_event_trigger_resource = google_pubsub_topic.bigquery_replication_topic.name
}

module "function_SportsAnalytics_Common_BigQuery_TestLoad" {
  source = "../modules/function"

  project_name = var.gcp_project_id
  function_name = "SportsAnalytics_Common_BigQuery_TestLoad"
  function_description = "Test data for testing the BigQuery replication function"
  function_deployment_bucket_name = google_storage_bucket.deploy_bucket.name
  function_entry_point = "bigquery_load_test"
  function_region = var.gcp_region
  function_runtime = "python39"
  function_available_memory_mb = 128
  function_trigger_http = true
  #function_event_trigger_type = "google.pubsub.topic.publish"
  #function_event_trigger_resource = google_pubsub_topic.bigquery_replication_topic.name
}



