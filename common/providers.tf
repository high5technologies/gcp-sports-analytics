terraform {
  required_providers {
    google = {
      source  = "hashicorp/google"
      version = "3.89.0"
    }
  }
  backend "remote" {
      # configured in env-config <env>_backend.conf files
  }
}

provider "google" {
  #project = "sports-analytics-dev"
  #region = "us-central1" 
  project = var.gcp_project_id
  region = var.gcp_region
}
