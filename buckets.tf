resource "google_storage_bucket" "test-bucket" {
  name = "test-bucket-github"
  location      = "US"
  force_destroy = true
}
