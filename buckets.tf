resource "google_storage_bucket" "test-bucket-1" {
  name = "test-bucket-github"
  location      = "US"
  force_destroy = true
}
