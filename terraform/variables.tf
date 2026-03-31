variable "aws_region" {
  default = "us-east-1"
}

variable "project_name" {
  default = "employee-management-system"
}

# S3
variable "frontend_bucket_name" {
  default = "${var.project_name}-frontend-bucket-12345"
}

# EC2 (MongoDB)
variable "ami_id" {
  default = "ami-0fc5d935ebf8bc3bc" # Ubuntu 22.04
}

variable "instance_type" {
  default = "t2.micro"
}

# Networking
variable "vpc_cidr" {
  default = "10.0.0.0/16"
}

variable "subnet_cidr" {
  default = "10.0.1.0/24"
}

# Lambda
variable "lambda_function_name" {
  default = "${var.project_name}-backend-lambda"
}

variable "lambda_handler" {
  default = "app.main.handler"
}

variable "lambda_runtime" {
  default = "python3.12"
}

# API Gateway
variable "api_gateway_name" {
  default = "${var.project_name}-api-gateway"
}