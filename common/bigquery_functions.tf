
##########################################################################################
# Google BigQuery:  Functions
##########################################################################################

resource "google_bigquery_routine" "common_fuzzy_jaro_wrinkler_distance" {
  dataset_id = google_bigquery_dataset.bq_dataset_common.dataset_id
  routine_id     = "fuzzy_jaro_wrinkler_distance"
  routine_type = "SCALAR_FUNCTION"
  language = "JAVASCRIPT"
  definition_body = file("${path.module}/bigquery/functions/fuzzy_jaro_wrinkler_distance.js")
  arguments {
    name = "a"
    data_type = "{\"typeKind\" :  \"STRING\"}"
  } 
  arguments {
    name = "b"
    data_type = "{\"typeKind\" :  \"STRING\"}"
  }

  return_type = "{\"typeKind\" :  \"NUMERIC\"}"
}