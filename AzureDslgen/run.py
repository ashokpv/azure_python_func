import os
import json
import template_generator
from collections import OrderedDict

postreqdata = json.loads(open(os.environ['req']).read())
response = open(os.environ['res'], 'w')
template = template_generator.generate(postreqdata)
response_body = OrderedDict()
response_body["status"] = "success"
response_body["message"] = "Mistral template generated successfully"
response_body["template"] = template
response.write(json.dumps(response_body))
response.close()