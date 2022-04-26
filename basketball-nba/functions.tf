module "SportsAnalytics_NBA_Source_NBACOM_Scraper" {
  source = "../modules/function"

  gcp_project_id = var.gcp_project_id
  function_name = "SportsAnalytics_NBA_SOURCE_NBACOM_Scraper"
  function_description = "Scraper for nba.com Games, Boxes and Play-by-Play"
  function_deployment_bucket_name = google_storage_bucket.deploy_bucket.name
  function_entry_point = "nba_nbacom_scraper"
  function_region = var.gcp_region
  function_runtime = "python39"
  function_available_memory_mb = 128
  function_timeout = 540
  function_trigger_http = true
  #function_event_trigger_resource = google_pubsub_topic.bigquery_replication_topic.name
}

module "SportsAnalytics_NBA_WORKER_NBACOM_Schedule_Scraper" {
  source = "../modules/function"

  gcp_project_id = var.gcp_project_id
  function_name = "SportsAnalytics_NBA_WORKER_NBACOM_Schedule_Scraper"
  function_description = "Scraper for nba.com schedule"
  function_deployment_bucket_name = google_storage_bucket.deploy_bucket.name
  function_entry_point = "nba_nbacom_worker_Schedule_scraper"
  function_region = var.gcp_region
  function_runtime = "python39"
  function_available_memory_mb = 128
  function_timeout = 540
  #function_trigger_http = true
  function_event_trigger_resource = google_pubsub_topic.nba_nbacom_dates_to_scrape_topic.name
}

module "SportsAnalytics_NBA_WORKER_NBACOM_IndividualGame_Scraper" {
  source = "../modules/function"

  gcp_project_id = var.gcp_project_id
  function_name = "SportsAnalytics_NBA_WORKER_NBACOM_IndividualGame_Scraper"
  function_description = "Scraper for nba.com individual games, Boxes and Play-by-Play"
  function_deployment_bucket_name = google_storage_bucket.deploy_bucket.name
  function_entry_point = "nba_nbacom_worker_individual_scraper"
  function_region = var.gcp_region
  function_runtime = "python39"
  function_available_memory_mb = 512
  function_timeout = 540
  #function_trigger_http = true
  function_event_trigger_resource = google_pubsub_topic.nba_nbacom_games_to_scrape_topic.name
}
