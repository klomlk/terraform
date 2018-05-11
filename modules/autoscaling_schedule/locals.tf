locals {
  valid_time = "${var.valid_time != "" ? var.valid_time : timeadd(timestamp(), var.valid_time_delay)}"
}

