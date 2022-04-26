
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
