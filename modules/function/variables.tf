variable "project_name" {
  type        = string
  description = "The Google Cloud Project"
  nullable    = false 
}

variable "function_name" {
  type        = string
  description = "Name of the function"
  nullable    = false 
}

variable "function_description" {
  type        = string
  description = "Description of the function"
  nullable    = false 
}

variable "function_entry_point" {
  type        = string
  description = "Name of primary function that will get called with GCP Function triggered"
  nullable    = false 
}

variable "function_region" {
  type        = string
  description = "GCP region of function to deploy to"
  default     = "us-central1"
  nullable    = false 
}

variable "function_runtime" {
  type        = string
  description = "Language and version"
  default     = "python39"
  nullable    = false 
  validation {
    condition     = contains(["python37", "python38", "python39"], var.function_runtime)
    error_message = "Valid values for var: function_runtime are [python37, python38, python39]."
  } 
}

variable "function_available_memory_mb" {
  type        = number
  description = "Available memory in mb for function"
  default     = 128
  nullable    = false 
}

variable "function_trigger_http" {
  type        = bool
  description = "trigger function via http"
  default     = false
  nullable    = false 
}

variable "function_event_trigger_type" {
  type        = string
  description = "Type of GCP resouces that triggers function"
  default     = "null"
  nullable    = true
  validation {
    condition     = contains(["google.pubsub.topic.publish"], var.function_event_trigger_type) || var.function_event_trigger_type == null
    error_message = "Valid values for var: function_event_trigger_type are [google.pubsub.topic.publish]."
  } 
}

variable "function_event_trigger_resource" {
  type        = string
  description = "Name of the resouce that triggers function"
  default     = "null"
  nullable    = true
}

