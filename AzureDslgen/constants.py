# Defined to get the appropriate template attribute for actions
base_template_action_id = "x-cs-template-action-name"

# app host port for Corestack URL to hit
heatstack_port = 18080
resource_inventory_port = 18087
corestack_identity_port = 18081

# Added parameters exclude in the template generation
EXCLUDE_INPUT_PARAMS = ["api-version", "resourceGroupName", "subscriptionId", "$expand", "x-amz-date", "x-amz-target", "X-Amz-Content-Sha256", "X-Amz-Algorithm", "X-Amz-Credential", "Action", "Version", "X-Amz-Date", "X-Amz-Security-Token", "X-Amz-Signature", "X-Amz-SignedHeaders"]
EXCLUDE_OUTPUT_PARAMS = ['error']


# Following are the template success message
success_resp = ['200', '201', '202', '204']
