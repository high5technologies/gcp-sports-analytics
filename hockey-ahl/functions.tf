module "SportsAnalytics_AHL_Reference_HockeyTech_Seasons" {
  source = "../modules/function"

  project_name = var.gcp_project_id
  function_name = "SportsAnalytics_AHL_Reference_HockeyTech_Seasons"
  function_description = "1 time load of reference data for AHL HockeyTech API"
  function_deployment_bucket_name = google_storage_bucket.deploy_bucket.name
  function_entry_point = "load_firestore_reference_ahl_hockeytech_seasons"
  function_region = var.gcp_region
  function_runtime = "python39"
  function_available_memory_mb = 128
  #function_timeout
  function_trigger_http = true
  #function_event_trigger_resource = google_pubsub_topic.bigquery_replication_topic.name
}

module "SportsAnalytics_AHL_Source_All" {
  source = "../modules/function"

  project_name = var.gcp_project_id
  function_name = "SportsAnalytics_AHL_Source_All"
  function_description = "Wrapper for all NBA scrapers - loads game dates to appropiate Queues for processing"
  function_deployment_bucket_name = google_storage_bucket.deploy_bucket.name
  function_entry_point = "ahl_all"
  function_region = var.gcp_region
  function_runtime = "python39"
  function_available_memory_mb = 128
  function_timeout = 540
  #function_trigger_http = true
  function_event_trigger_resource = google_pubsub_topic.ahl_scrape_all_topic.name
}

module "SportsAnalytics_AHL_WORKER_AHLCOM_Schedule_Scraper" {
  source = "../modules/function"

  project_name = var.gcp_project_id
  function_name = "SportsAnalytics_AHL_WORKER_AHLCOM_Schedule_Scraper"
  function_description = "Schedule Scraper for ahl.com Games, Boxes and Play-by-Play using HockeyTech API"
  function_deployment_bucket_name = google_storage_bucket.deploy_bucket.name
  function_entry_point = "ahl_ahlcom_worker_schedule_scraper"
  function_region = var.gcp_region
  function_runtime = "python39"
  function_available_memory_mb = 128
  function_timeout = 120
  #function_trigger_http = true
  function_event_trigger_resource = google_pubsub_topic.ahl_ahlcom_months_to_scrape_topic.name
}

module "SportsAnalytics_AHL_WORKER_AHLCOM_IndividualGame_Scraper" {
  source = "../modules/function"

  project_name = var.gcp_project_id
  function_name = "SportsAnalytics_AHL_WORKER_AHLCOM_IndividualGame_Scraper"
  function_description = "Scape an individual game key from AHL.com HockeyTech API"
  function_deployment_bucket_name = google_storage_bucket.deploy_bucket.name
  function_entry_point = "ahl_ahlcom_worker_individual_game_scraper"
  function_region = var.gcp_region
  function_runtime = "python39"
  function_available_memory_mb = 128
  function_timeout = 120
  #function_trigger_http = true
  function_event_trigger_resource = google_pubsub_topic.ahl_ahlcom_games_to_scrape_topic.name
}

module "SportsAnalytics_AHL_WORKER_AHLCOM_Roster_Season_Scraper" {
  source = "../modules/function"

  project_name = var.gcp_project_id
  function_name = "SportsAnalytics_AHL_WORKER_AHLCOM_Roster_Season_Scraper"
  function_description = "Scrape the teams within a season to get roster info"
  function_deployment_bucket_name = google_storage_bucket.deploy_bucket.name
  function_entry_point = "ahl_roster_season_scraper"
  function_region = var.gcp_region
  function_runtime = "python39"
  function_available_memory_mb = 128
  function_timeout = 120
  #function_trigger_http = true
  function_event_trigger_resource = google_pubsub_topic.ahl_ahlcom_roster_seasons_to_scrape_topic.name
}

module "SportsAnalytics_AHL_WORKER_AHLCOM_Roster_Team_Scraper" {
  source = "../modules/function"

  project_name = var.gcp_project_id
  function_name = "SportsAnalytics_AHL_WORKER_AHLCOM_Roster_Team_Scraper"
  function_description = "Scrape the team roster for a season"
  function_deployment_bucket_name = google_storage_bucket.deploy_bucket.name
  function_entry_point = "ahl_roster_team_scraper"
  function_region = var.gcp_region
  function_runtime = "python39"
  function_available_memory_mb = 128
  function_timeout = 120
  #function_trigger_http = true
  function_event_trigger_resource = google_pubsub_topic.ahl_ahlcom_roster_season_teams_to_scrape_topic.name
}






