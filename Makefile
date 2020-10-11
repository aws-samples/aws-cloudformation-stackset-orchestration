.PHONY: build package changes deploy help

build: ## Build the SAM application locally using an AWS Lamnbda-like container
	sam build --use-container

package: ## Package the SAM application and upload it to an s3 bucket along with its dependencies
	sam package --s3-prefix stackset-orchestration \
		   --s3-bucket $(s3_bucket) \
		   --output-template-file template-output.yaml

changes: build package ## View the SAM application changeset
	sam deploy --template-file template-output.yaml \
		   --stack-name stackset-orchestration \
		   --parameter-overrides \
		   StacksetAdministratorPrincipal=$(stackset_administrator_principal) \
		   --capabilities CAPABILITY_NAMED_IAM \
		   --no-execute-changeset

deploy: build package ## Deploy the SAM application
	sam deploy --template-file template-output.yaml \
		   --stack-name stackset-orchestration \
		   --parameter-overrides \
		   StackSetAdministratorPrincipal=$(stackset_administrator_principal) \
		   --capabilities CAPABILITY_NAMED_IAM

help: ## Display this help screen
	@grep -h -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'
