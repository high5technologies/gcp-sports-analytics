# Create bucket to deploy code to
#resource "google_storage_bucket" "mod_deploy_bucket" {
#  name = "function_deploy_${var.project_name}"
#  location      = "US"
#  #force_destroy = true
#}

# Zip the file path
data "archive_file" "mod_zip" {
  type        = "zip"
  #source_dir = "${path.module}/${var.function_name}/"
  #output_path = "${path.module}/${var.function_name}.zip"
  source_dir = "functions/${var.function_name}/"
  output_path = "functions/${var.function_name}.zip"
}

# Upload zip to bucket
resource "google_storage_bucket_object" "mod_archive_object" {
  #name   = "terraform-google-functions-zips/${var.function_name}_${local.timestamp}.zip"
  name   = format("terraform-google-functions-zips/${var.function_name}_%s.zip", data.archive_file.mod_zip.output_md5)
  #bucket = google_storage_bucket.mod_deploy_bucket.name
  bucket = var.function_deployment_bucket_name
  source = data.archive_file.mod_zip.output_path
  #deletion_protection=false
}

resource "google_cloudfunctions_function" "mod_function" {
  name        = var.function_name
  description = var.function_description
  runtime     = var.function_runtime

  available_memory_mb   = var.function_available_memory_mb
  timeout               = var.function_timeout
  #source_archive_bucket = google_storage_bucket.mod_deploy_bucket.name
  source_archive_bucket = var.function_deployment_bucket_name
  source_archive_object = google_storage_bucket_object.mod_archive_object.name
  trigger_http          = var.function_trigger_http
  entry_point           = var.function_entry_point
  region                = var.function_region

  environment_variables = {
    FUNCTION_NAME  = var.function_name
    GCP_PROJECT_ID = var.gcp_project_id
  }
  #event_trigger {
  #  event_type = var.function_event_trigger_type
  #  resource = var.function_event_trigger_resource
  #}
  dynamic "event_trigger" {
      for_each = var.function_event_trigger_resource[*]
      content {
         #event_type = var.function_event_trigger_type
         event_type = "google.pubsub.topic.publish"
         resource   = var.function_event_trigger_resource
      }
   }
}

# IAM entry for all users to invoke the function
#resource "google_cloudfunctions_function_iam_member" "mod_invoker_permissions" {
#  project        = google_cloudfunctions_function.mod_function.project
#  region         = google_cloudfunctions_function.mod_function.region
#  cloud_function = google_cloudfunctions_function.mod_function.name
#
#  role   = "roles/cloudfunctions.invoker"
#  member = "allUsers"
#}
