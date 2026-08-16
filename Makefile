TF_DIR := infra/app
AWS_CONFIRM_VALUE := I_ACCEPT_AWS_CHARGES

.PHONY: infra-init infra-fmt infra-validate infra-check
.PHONY: aws-confirm aws-plan aws-up aws-down


# ----------------------------------
# Safe local Terraform commands
# ----------------------------------

infra-init:
	terraform -chdir=$(TF_DIR) init -backend=false

infra-fmt:
	terraform -chdir=$(TF_DIR) fmt -check

infra-validate:
	terraform -chdir=$(TF_DIR) validate

infra-check: infra-init infra-fmt infra-validate
	@echo "PolyText Terraform configuration is valid."


# ----------------------------------
# AWS safety gate
# ----------------------------------

aws-confirm:
	@if [ "$(AWS_CONFIRM)" != "$(AWS_CONFIRM_VALUE)" ]; then \
		echo ""; \
		echo "AWS operation blocked."; \
		echo "This command may interact with resources that can incur AWS charges."; \
		echo ""; \
		echo "To explicitly allow it, run:"; \
		echo "AWS_CONFIRM=$(AWS_CONFIRM_VALUE) make <target>"; \
		echo ""; \
		exit 1; \
	fi


# ----------------------------------
# AWS commands
# ----------------------------------

aws-plan: aws-confirm
	terraform -chdir=$(TF_DIR) init
	terraform -chdir=$(TF_DIR) plan

aws-up: aws-confirm
	terraform -chdir=$(TF_DIR) init
	terraform -chdir=$(TF_DIR) apply

aws-down: aws-confirm
	terraform -chdir=$(TF_DIR) init
	terraform -chdir=$(TF_DIR) destroy
