provider "google" {
  #project = var.project_id
  project = "sports-analytics-dev"
  #region  = var.region
  region = "us-central1" 
}

#terraform {
#  backend "gcs" {
#    bucket = "myvik-tf-state-prod"
#    prefix = "terraform/state"
#  }
#}

# Using a single workspace:
terraform {
  backend "remote" {
    hostname = "app.terraform.io"
    organization = "high5"

    workspaces {
      name = "gcp-sports-analytics"
    }
  }
}
