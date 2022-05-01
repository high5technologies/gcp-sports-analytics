
##########################################################################################
# Pub Sub Topics
##########################################################################################

# NBA.COM Games to scrape
resource "google_pubsub_topic" "nba_nbacom_dates_to_scrape_topic" {
  name = "nba_nbacom_dates_to_scrape"
}
resource "google_pubsub_topic" "nba_nbacom_games_to_scrape_topic" {
  name = "nba_nbacom_games_to_scrape"
}

# NBASTATS Dates to scrape
resource "google_pubsub_topic" "nba_nbastats_dates_to_scrape_topic" {
  name = "nba_nbastats_dates_to_scrape"
}

# Espn Games to scrape
resource "google_pubsub_topic" "nba_espn_dates_to_scrape_topic" {
  name = "nba_espn_dates_to_scrape"
}

# Espn Game to scrape - Game Cast
resource "google_pubsub_topic" "nba_espn_games_to_scrape_gamecast_topic" {
  name = "nba_espn_games_to_scrape_gamecast"
}

# Espn Game to scrape - Play By Play
resource "google_pubsub_topic" "nba_espn_games_to_scrape_playbyplay_topic" {
  name = "nba_espn_games_to_scrape_playbyplay"
}

# SportsBookReview.COM (SBR) Games to scrape
resource "google_pubsub_topic" "nba_sbr_dates_to_scrape_topic" {
  name = "nba_sbr_dates_to_scrape"
}
resource "google_pubsub_topic" "nba_sbr_games_to_scrape_topic" {
  name = "nba_sbr_games_to_scrape"
}

# 538 - Player Raptor
resource "google_pubsub_topic" "nba_538_playerraptor_seasons_to_scrape_topic" {
  name = "nba_538_playerraptor_seasons_to_scrape"
}

# 538 - Predictions
resource "google_pubsub_topic" "nba_538_predictions_range_to_scrape_topic" {
  name = "nba_538_predictions_range_to_scrape"
}

resource "google_pubsub_topic" "nba_scrape_all_topic" {
  name = "nba_scrape_all"
}