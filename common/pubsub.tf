# Google Pubsup Topic: BigQuery Replication
resource "google_pubsub_topic" "bigquery_replication_topic_" {
  name = "bigquery_replication_topic"
}

# Google Pubsup Topic: BigQuery Replication
resource "google_pubsub_topic" "error_log_topic_" {
  name = "error_log_topic"
}

# Test for function 
#resource "google_pubsub_topic" "common_test_topic" {
#  name = "common_test_topic"
#}

