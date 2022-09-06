# Google Pubsup Topic: BigQuery Replication
resource "google_pubsub_topic" "bigquery_replication_topic" {
  name = "bigquery_replication_topic"
}

# Google Pubsup Topic: BigQuery Replication
resource "google_pubsub_topic" "error_log_topic" {
  name = "error_log_topic"
}

# Google Pubsup Topic: BigQuery ReverseETL
resource "google_pubsub_topic" "bigquery_dates_to_reverseetl_topic" {
  name = "bigquery_dates_to_reverseetl"
}

resource "google_pubsub_topic" "bigquery_datastore_reverseetl_topic" {
  name = "bigquery_datastore_reverseetl"
}

# Test for function 
#resource "google_pubsub_topic" "common_test_topic" {
#  name = "common_test_topic"
#}

