variable "github_token" {
  sensitive = true
  type      = string
}

variable "github_org" {
  type = string
  default = "awalford16"
}

variable "github_repository" {
  type = string
}
