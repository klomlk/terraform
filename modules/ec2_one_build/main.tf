resource "aws_instance" "instance" {
  count                       = "${var.instance_count}"
  subnet_id                   = "${var.subnets_id}"
  instance_type               = "${var.instance_type}"
  ami                         = "${var.ami}"
  disable_api_termination     = "${var.termination_protection}"
  key_name                    = "${var.key_name}"
  user_data                   = "${var.user_data}"
  iam_instance_profile        = "${var.iam_instance_profile}"
  vpc_security_group_ids      = ["${var.sg}"]
  associate_public_ip_address = "${var.associate_public_ip}"
  ebs_optimized               = "${var.ebs_optimized}"
  root_block_device {
    volume_size = "${var.volume_size}"
    volume_type = "${var.volume_type}"
  }
  volume_tags = "${merge(var.tags, var.ec2_tags,
  map("Name",format("%s - disk", var.ec2_tags["Hostname"]))
  )
  }"

  tags = "${merge(var.tags, var.ec2_tags,
  map("Name",format("%s - %s - %s - %s", var.tags["Environment"], var.ec2_tags["Hostname"], var.tags["Application"], var.ec2_tags["Role"]))
  )
  }"
}
