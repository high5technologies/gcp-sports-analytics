terraform {
  required_providers {
    google = {
      source  = "hashicorp/google"
      version = "3.89.0"
    }
  }
  backend "remote" {
    organization = "high5"

    workspaces {
      name = "gcp-sports-analytics"
    }
  }
}
provider "google" {
  project = "sports-analytics-dev"
  region = "us-central1" 
}
