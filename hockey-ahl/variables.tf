variable "gcp_project_id" {
  type        = string
  description = "The Google Cloud Project Id"
}

variable "gcp_region" {
  type    = string
  #default = "europe-west2"
  description = "The Google Cloud region"
}

variable "env" {
  type    = string
  description = "Environment being deployed to"
}