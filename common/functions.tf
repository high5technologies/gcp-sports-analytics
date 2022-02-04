module "s3-website" {
  source = "../modules/function"

  project_name = var.gcp_project_id
  function_name = "SportsAnalytics_Common_Test"
  function_description = "Test function"
  function_entry_point = "hello_world"
  function_region = var.gcp_region
  function_runtime = "python39"
  function_available_memory_mb = "128"
  function_trigger_http = false
  function_event_trigger_type = "google.pubsub.topic.publish"
  function_event_trigger_resource = google_pubsub_topic.common_test_topic.name
}
