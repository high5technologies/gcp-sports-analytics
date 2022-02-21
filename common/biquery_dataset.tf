resource "google_bigquery_dataset" "bq_dataset_common" {
  dataset_id                  = "common"
  friendly_name               = "common"
  description                 = "Data set for common"
  location                    = "US"
  #default_table_expiration_ms = 3600000

  labels = {
    env = var.env
    project = "sports_analytics"
  }
}
