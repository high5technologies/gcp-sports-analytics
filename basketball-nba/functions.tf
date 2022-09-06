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

module "SportsAnalytics_NBA_SOURCE_538_Scraper" {
  source = "../modules/function"

  gcp_project_id = var.gcp_project_id
  function_name = "SportsAnalytics_NBA_SOURCE_538_Scraper"
  function_description = "Scraper for NBA 538 predictions"
  function_deployment_bucket_name = google_storage_bucket.deploy_bucket.name
  function_entry_point = "nba_538_scraper"
  function_region = var.gcp_region
  function_runtime = "python39"
  function_available_memory_mb = 4096
  function_timeout = 540
  function_trigger_http = true
  #function_event_trigger_resource = google_pubsub_topic.bigquery_replication_topic.name
}

module "SportsAnalytics_NBA_WORKER_538_Prediction_Scraper" {
  source = "../modules/function"

  gcp_project_id = var.gcp_project_id
  function_name = "SportsAnalytics_NBA_WORKER_538_Prediction_Scraper"
  function_description = "Scraper for 538 Prediction CSV from GITHUB"
  function_deployment_bucket_name = google_storage_bucket.deploy_bucket.name
  function_entry_point = "nba_538_prediction_worker"
  function_region = var.gcp_region
  function_runtime = "python39"
  function_available_memory_mb = 512
  function_timeout = 540
  #function_trigger_http = true
  function_event_trigger_resource = google_pubsub_topic.nba_538_predictions_range_to_scrape_topic.name
}

module "SportsAnalytics_NBA_SOURCE_538_PlayerRaptor_Scraper" {
  source = "../modules/function"

  gcp_project_id = var.gcp_project_id
  function_name = "SportsAnalytics_NBA_SOURCE_538_PlayerRaptor_Scraper"
  function_description = "Scraper for NBA 538 Player Raptor predictions - individual raptor player projections"
  function_deployment_bucket_name = google_storage_bucket.deploy_bucket.name
  function_entry_point = "nba_538_PlayerRaptor_scraper"
  function_region = var.gcp_region
  function_runtime = "python39"
  function_available_memory_mb = 4096
  function_timeout = 540
  function_trigger_http = true
  #function_event_trigger_resource = google_pubsub_topic.nba_538_predictions_range_to_scrape_topic.name
}

module "SportsAnalytics_NBA_WORKER_538_PlayerRaptor_Scraper" {
  source = "../modules/function"

  gcp_project_id = var.gcp_project_id
  function_name = "SportsAnalytics_NBA_WORKER_538_PlayerRaptor_Scraper"
  function_description = "Scraper for 538 Player Raptor CSV from GITHUB"
  function_deployment_bucket_name = google_storage_bucket.deploy_bucket.name
  function_entry_point = "nba_538_player_raptor_worker"
  function_region = var.gcp_region
  function_runtime = "python39"
  function_available_memory_mb = 512
  function_timeout = 540
  #function_trigger_http = true
  function_event_trigger_resource = google_pubsub_topic.nba_538_playerraptor_seasons_to_scrape_topic.name
}

module "SportsAnalytics_NBA_SOURCE_SBR_Scraper" {
  source = "../modules/function"

  gcp_project_id = var.gcp_project_id
  function_name = "SportsAnalytics_NBA_SOURCE_SBR_Scraper"
  function_description = "Scraper for NBA SBR Games and boxes"
  function_deployment_bucket_name = google_storage_bucket.deploy_bucket.name
  function_entry_point = "nba_sbr_scraper"
  function_region = var.gcp_region
  function_runtime = "python39"
  function_available_memory_mb = 128
  function_timeout = 540
  function_trigger_http = true
  #function_event_trigger_resource = google_pubsub_topic.nba_538_playerraptor_seasons_to_scrape_topic.name
}

module "SportsAnalytics_NBA_WORKER_SBR_Schedule_Scraper" {
  source = "../modules/function"

  gcp_project_id = var.gcp_project_id
  function_name = "SportsAnalytics_NBA_WORKER_SBR_Schedule_Scraper"
  function_description = "Scraper for SBR.com Games, Boxes and Play-by-Play"
  function_deployment_bucket_name = google_storage_bucket.deploy_bucket.name
  function_entry_point = "nba_sbr_worker_Schedule_scraper"
  function_region = var.gcp_region
  function_runtime = "python39"
  function_available_memory_mb = 128
  function_timeout = 540
  #function_trigger_http = true
  function_event_trigger_resource = google_pubsub_topic.nba_sbr_dates_to_scrape_topic.name
}

module "SportsAnalytics_NBA_WORKER_SBR_IndividualGame_Scraper" {
  source = "../modules/function"

  gcp_project_id = var.gcp_project_id
  function_name = "SportsAnalytics_NBA_WORKER_SBR_IndividualGame_Scraper"
  function_description = "Scraper for SBR.com Games, Boxes and Play-by-Play"
  function_deployment_bucket_name = google_storage_bucket.deploy_bucket.name
  function_entry_point = "nba_sbr_worker_individual_scraper"
  function_region = var.gcp_region
  function_runtime = "python39"
  function_available_memory_mb = 512
  function_timeout = 540
  #function_trigger_http = true
  function_event_trigger_resource = google_pubsub_topic.nba_sbr_games_to_scrape_topic.name
}

module "SportsAnalytics_NBA_WORKER_ESPN_Schedule_Scraper" {
  source = "../modules/function"

  gcp_project_id = var.gcp_project_id
  function_name = "SportsAnalytics_NBA_WORKER_ESPN_Schedule_Scraper"
  function_description = "Scraper for ESPN data from gamecast pagey"
  function_deployment_bucket_name = google_storage_bucket.deploy_bucket.name
  function_entry_point = "nba_espn_worker_Schedule_scraper"
  function_region = var.gcp_region
  function_runtime = "python39"
  function_available_memory_mb = 128
  function_timeout = 540
  #function_trigger_http = true
  function_event_trigger_resource = google_pubsub_topic.nba_espn_dates_to_scrape_topic.name
}

module "SportsAnalytics_NBA_WORKER_ESPN_IndividualGameCast_Scraper" {
  source = "../modules/function"

  gcp_project_id = var.gcp_project_id
  function_name = "SportsAnalytics_NBA_WORKER_ESPN_IndividualGameCast_Scraper"
  function_description = "Scraper for iindividual espn game cast page"
  function_deployment_bucket_name = google_storage_bucket.deploy_bucket.name
  function_entry_point = "nba_espn_worker_individual_gamecast_scraper"
  function_region = var.gcp_region
  function_runtime = "python39"
  function_available_memory_mb = 512
  function_timeout = 540
  #function_trigger_http = true
  function_event_trigger_resource = google_pubsub_topic.nba_espn_games_to_scrape_gamecast_topic.name
}

module "SportsAnalytics_NBA_WORKER_ESPN_IndividualPlayByPlay_Scraper" {
  source = "../modules/function"

  gcp_project_id = var.gcp_project_id
  function_name = "SportsAnalytics_NBA_WORKER_ESPN_IndividualPlayByPlay_Scraper"
  function_description = "Scraper for iindividual espn game play by play page"
  function_deployment_bucket_name = google_storage_bucket.deploy_bucket.name
  function_entry_point = "nba_espn_worker_individual_playbyplay_scraper"
  function_region = var.gcp_region
  function_runtime = "python39"
  function_available_memory_mb = 512
  function_timeout = 540
  #function_trigger_http = true
  function_event_trigger_resource = google_pubsub_topic.nba_espn_games_to_scrape_playbyplay_topic.name
}

module "SportsAnalytics_NBA_SOURCE_BasketballReference_Scraper" {
  source = "../modules/function"

  gcp_project_id = var.gcp_project_id
  function_name = "SportsAnalytics_NBA_SOURCE_BasketballReference_Scraper"
  function_description = "Scraper for NBA BasketballReference Games and boxes"
  function_deployment_bucket_name = google_storage_bucket.deploy_bucket.name
  function_entry_point = "nba_basketballreference_scraper"
  function_region = var.gcp_region
  function_runtime = "python39"
  function_available_memory_mb = 512
  function_timeout = 540
  function_trigger_http = true
  #function_event_trigger_resource = google_pubsub_topic.nba_espn_games_to_scrape_playbyplay_topic.name
}

module "SportsAnalytics_NBA_SOURCE_ALL" {
  source = "../modules/function"

  gcp_project_id = var.gcp_project_id
  function_name = "SportsAnalytics_NBA_SOURCE_ALL"
  function_description = "Wrapper for all NBA scrapers - loads game dates to appropiate Queues for processing"
  function_deployment_bucket_name = google_storage_bucket.deploy_bucket.name
  function_entry_point = "nba_all"
  function_region = var.gcp_region
  function_runtime = "python39"
  function_available_memory_mb = 128
  function_timeout = 540
  #function_trigger_http = true
  function_event_trigger_resource = google_pubsub_topic.nba_scrape_all_topic.name
}


module "SportsAnalytics_NBA_SOURCE_NBASTATS_Scraper" {
  source = "../modules/function"

  gcp_project_id = var.gcp_project_id
  function_name = "SportsAnalytics_NBA_SOURCE_NBASTATS_Scraper"
  function_description = "All APIs from stats.nba.com"
  function_deployment_bucket_name = google_storage_bucket.deploy_bucket.name
  function_entry_point = "nba_nbastats_scraper"
  function_region = var.gcp_region
  function_runtime = "python39"
  function_available_memory_mb = 512
  function_timeout = 540
  function_trigger_http = true
  #function_event_trigger_resource = google_pubsub_topic.nba_nbastats_dates_to_scrape_topic.name
}

module "SportsAnalytics_NBA_WORKER_NBASTATS_Game_Scraper" {
  source = "../modules/function"

  gcp_project_id = var.gcp_project_id
  function_name = "SportsAnalytics_NBA_WORKER_NBASTATS_Game_Scraper"
  function_description = "API for stats.nba.com - Game"
  function_deployment_bucket_name = google_storage_bucket.deploy_bucket.name
  function_entry_point = "nba_nbastats_worker_scraper"
  function_region = var.gcp_region
  function_runtime = "python39"
  function_available_memory_mb = 512
  function_timeout = 540
  #function_trigger_http = true
  function_event_trigger_resource = google_pubsub_topic.nba_nbastats_dates_to_scrape_topic.name
}

module "SportsAnalytics_NBA_SOURCE_Swish_Salary_Scraper" {
  source = "../modules/function"

  gcp_project_id = var.gcp_project_id
  function_name = "SportsAnalytics_NBA_SOURCE_Swish_Salary_Scraper"
  function_description = "Source scraper for Swish Salaries"
  function_deployment_bucket_name = google_storage_bucket.deploy_bucket.name
  function_entry_point = "nba_swish_salary_scraper"
  function_region = var.gcp_region
  function_runtime = "python39"
  function_available_memory_mb = 512
  function_timeout = 540
  #function_trigger_http = true
  function_event_trigger_resource = google_pubsub_topic.nba_swish_source_topic.name
}

module "SportsAnalytics_NBA_WORKER_Swish_IndividualDFSSalary_Scraper" {
  source = "../modules/function"

  gcp_project_id = var.gcp_project_id
  function_name = "SportsAnalytics_NBA_WORKER_Swish_IndividualDFSSalary_Scraper"
  function_description = "Individual game scraper for Swish Analytics Salaries"
  function_deployment_bucket_name = google_storage_bucket.deploy_bucket.name
  function_entry_point = "nba_swish_worker_individual_dfssalary_scraper"
  function_region = var.gcp_region
  function_runtime = "python39"
  function_available_memory_mb = 512
  function_timeout = 540
  #function_trigger_http = true
  function_event_trigger_resource = google_pubsub_topic.nba_swish_salaries_dates_to_scrape_topic.name
}
