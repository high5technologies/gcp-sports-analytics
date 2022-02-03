variable "gcp_project_id" {
  type        = string
  description = "The Google Cloud Project Id"
}

variable "gcp_region" {
  type    = string
  #default = "europe-west2"
  description = "The Google Cloud region"
}

variable "tfcloud_organization" {
    type        = string
    description = "Terraform Cloud Organization - State File"
}

variable "tfcloud_workspace" {
    type        = string
    description = "Terraform Cloud Workspace name - State File"
}
