variable "subscription_id" {
  description = "Azure subscription ID to deploy into (az account show --query id -o tsv)."
  type        = string
}

variable "location" {
  description = "Azure region for all resources."
  type        = string
  default     = "australiaeast"
}

variable "project" {
  description = "Short lowercase name used as a prefix for resource names."
  type        = string
  default     = "sydhousing"

  validation {
    condition     = can(regex("^[a-z0-9]{3,12}$", var.project))
    error_message = "project must be 3 to 12 lowercase letters or digits (it is used in the container registry name)."
  }
}

variable "github_repository" {
  description = "GitHub repository (owner/name) allowed to deploy through OIDC."
  type        = string
  default     = "rohitbondala277/Sydney-Housing"
}

variable "github_branch" {
  description = "Branch whose workflow runs are allowed to deploy."
  type        = string
  default     = "main"
}

variable "deploy_app" {
  description = "Create the Container App. Leave false on the first apply, push to main so the pipeline builds the first image, then set to true."
  type        = bool
  default     = false
}

variable "image_name" {
  description = "Repository name of the app image inside the container registry."
  type        = string
  default     = "sydney-housing"
}

variable "max_replicas" {
  description = "Upper limit for autoscaling. The app scales to zero when idle."
  type        = number
  default     = 2
}
