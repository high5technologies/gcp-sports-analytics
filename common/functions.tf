module "SportsAnalytics_Common_Log_Error" {
  source = "../modules/function"

  gcp_project_id = var.gcp_project_id
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

module "SportsAnalytics_Common_BigQuery_Replication" {
  source = "../modules/function"

  gcp_project_id = var.gcp_project_id
  function_name = "SportsAnalytics_Common_BigQuery_Replication"
  function_description = "Replication pubsub message to BigQuery"
  function_deployment_bucket_name = google_storage_bucket.deploy_bucket.name
  function_entry_point = "pubsub_to_bigquery_replication"
  function_region = var.gcp_region
  function_runtime = "python39"
  function_available_memory_mb = 2048
  #function_trigger_http = null
  #function_event_trigger_type = "google.pubsub.topic.publish"
  function_event_trigger_resource = google_pubsub_topic.bigquery_replication_topic.name
}

module "SportsAnalytics_Common_BigQuery_TestLoad" {
  source = "../modules/function"

  gcp_project_id = var.gcp_project_id
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


module "SportsAnalytics_Common_BigQuery_Datastore_ReverseETL" {
  source = "../modules/function"

  gcp_project_id = var.gcp_project_id
  function_name = "SportsAnalytics_Common_BigQuery_Datastore_ReverseETL"
  function_description = "Reverse ETL for BigQuery to Datastore - configurable"
  function_deployment_bucket_name = google_storage_bucket.deploy_bucket.name
  function_entry_point = "bigquery_datastore_reverseetl"
  function_region = var.gcp_region
  function_runtime = "python39"
  function_available_memory_mb = 512
  function_timeout = 540
  #function_trigger_http = true
  function_event_trigger_resource = google_pubsub_topic.bigquery_datastore_reverseetl_topic.name
}




#module "function_SportsAnalytics_Common_BigQuery_Dates_To_ReverseETL" {
#  source = "../modules/function"
#
#  gcp_project_id = var.gcp_project_id
#  function_name = "SportsAnalytics_Common_BigQuery_Dates_To_ReverseETL"
#  function_description = "Dates to push events to for Reverse ETL"
#  function_deployment_bucket_name = google_storage_bucket.deploy_bucket.name
#  function_entry_point = "dates_to_reverseetl"
#  function_region = var.gcp_region
#  function_runtime = "python39"
#  function_available_memory_mb = 512
#  #function_trigger_http = true
#  function_event_trigger_resource = google_pubsub_topic.bigquery_dates_to_reverseetl_topic.name
#}

