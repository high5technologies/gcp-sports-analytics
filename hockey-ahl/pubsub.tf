resource "google_pubsub_topic" "ahl_scrape_all_topic" {
  name = "ahl_scrape_all"
}

resource "google_pubsub_topic" "ahl_ahlcom_months_to_scrape_topic" {
  name = "ahl_ahlcom_months_to_scrape"
}

resource "google_pubsub_topic" "ahl_ahlcom_games_to_scrape_topic" {
  name = "ahl_ahlcom_games_to_scrape"
}

resource "google_pubsub_topic" "ahl_ahlcom_roster_seasons_to_scrape_topic" {
  name = "ahl_ahlcom_roster_seasons_to_scrape"
}

resource "google_pubsub_topic" "ahl_ahlcom_roster_season_teams_to_scrape_topic" {
  name = "ahl_ahlcom_roster_season_teams_to_scrape"
}