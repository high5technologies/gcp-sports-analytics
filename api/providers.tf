terraform {
  required_providers {
    google = {
      source  = "hashicorp/google"
      version = "4.21.0"
    }
    google-beta = {
      source  = "hashicorp/google-beta"
      version = "4.21.0"
    }
  }
  backend "remote" {
    #organization = "high5"
    #organization = var.tfcloud_organization

    #workspaces {
    #  #name = "gcp-sports-analytics"
    #  name = var.tfcloud_workspace
    #}
  }
}

provider "google" {
  #project = "sports-analytics-dev"
  #region = "us-central1" 
  project = var.gcp_project_id
  region = var.gcp_region
}

provider "google-beta" {
  project = var.gcp_project_id
  region = var.gcp_region
}
