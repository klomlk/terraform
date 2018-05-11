variable "count" { default = 0 }
variable "scheduled_action_name" {}
variable "min_size" {}
variable "max_size" {}
variable "desired_capacity" {}
variable "autoscaling_group_name" {}
variable "recurrence" {}
variable "recurrence_start" { default = "0 5 * * Mon-Fri"}
variable "recurrence_stop" { default = "0 21 * * Mon-Fri"}
variable "valid_time" { 
  default = "" 
}
variable "valid_time_delay" {
default = "10m"
}
