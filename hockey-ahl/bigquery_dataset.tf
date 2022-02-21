
##########################################################################################
# Google BigQuery:  Data Set
##########################################################################################

resource "google_bigquery_dataset" "bq_dataset_ahl" {
  dataset_id                  = "ahl"
  friendly_name               = "ahl"
  description                 = "Data set for ahl"
  location                    = "US"
  #default_table_expiration_ms = 3600000

  labels = {
    env = var.env
    project = "sports_analytics"
  }
}
