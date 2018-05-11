variable "ami" {}
variable "instance_type" {}
variable "key_name" {}
variable "user_data" {}
variable "ebs_optimized" {
  default = "false"
}
variable "volume_size" { default = "30" }
variable "volume_type" { default = "gp2" }
variable "iam_instance_profile" {
  default = ""
}

variable "sg" {
  type    = "list"
  default = [""]
}

variable "subnets_id" {}

variable "associate_public_ip" {
  default = "false"
}

variable "termination_protection" {
  default = "false"
}

variable "tags" {
  type    = "map"
  default = {}
}

variable "ec2_tags" {
  type = "map"
}

variable "instance_count" {
  default = "1"
}

#default = {
#  "Hostname"         = "Not available at build"
#  "Role"             = "Not available at build"
#  "OS"               = "Not available at build"
#  "Auto-stop"        = "none"
#  "Auto-start"       = "none"
#  "Backup_policy"    = "Standard"
#  "Backup_retention" = "30"
#}

