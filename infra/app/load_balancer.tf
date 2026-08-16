resource "aws_lb" "polytext" {
  name               = "${local.name_prefix}-alb"
  internal           = false
  load_balancer_type = "application"

  security_groups = [
    aws_security_group.alb.id
  ]

  subnets = [
    aws_subnet.public_a.id,
    aws_subnet.public_b.id
  ]

  enable_deletion_protection = false

  tags = local.common_tags
}


resource "aws_lb_target_group" "polytext" {
  name        = "${local.name_prefix}-tg"
  port        = 8000
  protocol    = "HTTP"
  target_type = "ip"
  vpc_id      = aws_vpc.main.id

  health_check {
    enabled             = true
    path                = "/ready"
    protocol            = "HTTP"
    port                = "traffic-port"
    matcher             = "200"
    interval            = 30
    timeout             = 5
    healthy_threshold   = 2
    unhealthy_threshold = 2
  }

  tags = local.common_tags
}


resource "aws_lb_listener" "http" {
  load_balancer_arn = aws_lb.polytext.arn
  port              = 80
  protocol          = "HTTP"

  default_action {
    type             = "forward"
    target_group_arn = aws_lb_target_group.polytext.arn
  }
}
