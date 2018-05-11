output "subnets_id" {
  value = "${var.subnets_id}"
}

output "instance_id" {
  value = "${element(concat(aws_instance.instance.*.id, list("")), 0)}"
}
