terraform {
  required_providers {
    random = {
      source  = "hashicorp/random"
      version = "3.0.1"
    }
  }
  required_version = ">= 1.1.0"

  cloud {
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
