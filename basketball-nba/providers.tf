terraform {
  required_providers {
    google = {
      source  = "hashicorp/google"
      version = "3.89.0"
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
