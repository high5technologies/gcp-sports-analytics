module "SportsAnalytics_API_Get_Dataset" {
  source = "../modules/function"

  gcp_project_id = var.gcp_project_id
  function_name = "SportsAnalytics_API_Get_Dataset"
  function_description = "Function to retrieve datasets for Sports Analytics API"
  function_deployment_bucket_name = google_storage_bucket.deploy_bucket.name
  function_entry_point = "api_return_data"
  function_region = var.gcp_region
  function_runtime = "python39"
  function_available_memory_mb = 512
  function_timeout = 30
  function_trigger_http = true
  #function_event_trigger_resource = google_pubsub_topic.bigquery_dates_to_reverseetl_topic.name
}