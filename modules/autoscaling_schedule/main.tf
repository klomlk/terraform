resource "aws_autoscaling_schedule" "stop" {
  count = "${var.count ? 1 : 0}"
  scheduled_action_name = "${var.scheduled_action_name}-stop"
  min_size = 0
  max_size = 0
  desired_capacity = 0
  start_time = "${local.valid_time}"
  autoscaling_group_name = "${var.autoscaling_group_name}"
  recurrence = "${var.recurrence_stop}"
  lifecycle {
    ignore_changes = ["start_time"]
  }
}
resource "aws_autoscaling_schedule" "start" {
  count = "${var.count ? 1 : 0}"
  scheduled_action_name = "${var.scheduled_action_name}-start"
  min_size = "${var.min_size}"
  max_size = "${var.max_size}"
  desired_capacity = "${var.desired_capacity}"
  start_time = "${timeadd(local.valid_time,"1s")}"
  autoscaling_group_name = "${var.autoscaling_group_name}"
  recurrence = "${var.recurrence_start}"
  lifecycle {
    ignore_changes = ["start_time"]
  }
}
