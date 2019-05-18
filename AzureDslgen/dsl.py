import template_generator
from collections import OrderedDict


def lambda_handler(event, context):
    # Executing the api from lambda
    template = template_generator.generate(event)
    response = OrderedDict()
    response["status"] = "success"
    response["message"] = "Mistral template generated successfully"
    response["template"] = template
    return response
