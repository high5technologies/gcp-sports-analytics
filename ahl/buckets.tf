resource "google_storage_bucket" "test-bucket-1" {
  name = "test-bucket-github-1"
  location      = "US"
  force_destroy = true
}

resource "google_storage_bucket" "test-bucket-4" {
  name = "test-bucket-github-4"
  location      = "US"
  force_destroy = true
}

