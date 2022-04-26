
##########################################################################################
# Google BigQuery:  Data Set
##########################################################################################

resource "google_bigquery_dataset" "bq_dataset_nba" {
  dataset_id                  = "nba"
  friendly_name               = "nba"
  description                 = "Data set for nba"
  location                    = "US"
  #default_table_expiration_ms = 3600000
  
  labels = {
    env = var.env
    project = "sports_analytics"
    league = "nba"
  }
}
