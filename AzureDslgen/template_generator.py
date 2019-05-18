import json
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname( __file__ ), 'myvenv/Lib/site-packages')))

import httplib2
import constants
from swagger_parser import get_details
from mistral import generate_template, create_template


def internal_api(url, host, resource_inventory=False):
    """
    Internal api to get the resource data
    :param url:
    :param host:
    :param resource_inventory:
    :return:
    """
    print "internal api"
    port = constants.heatstack_port
    if resource_inventory:
        port = constants.resource_inventory_port
    url_prefix = "{}:{}".format(host, port)
    url = url_prefix + url
    try:
        httpclient = httplib2.Http()
        headers = {"Content-Type": "application/json"}
        print url
        print headers
    
        response, body = httpclient.request(url, method="GET", headers=headers)
        print response
        print body
        re = json.loads(body)
        return re
    except Exception:
        raise Exception("Error in internal api")


def generate(req):
    try:
        body = req["operations"]
        template = list()
        task_name = desc = service_name = None
        host = req.get("host")
        service_id = req.get("service_id")
        project_id = req.get("project_id")
        operations_list = req.get("operations")
        if not service_id:
            raise Exception("Service_id is Empty/Invalid")
        print body
        for operation_id, values in body.iteritems():
            for k, v in operations_list.iteritems():
                url = "/v2/cloud/{}/service_schema?operation_id={}".format(str(service_id), k)
                swagger_schema_data = internal_api(url, host, resource_inventory=True)
                schema = swagger_schema_data["data"]["service_schema"]
                service_name = swagger_schema_data["data"]["service_name"]
                task_name, desc, params, outputs = get_details(schema, operation_id)
            r_input = values.get('input')
            r_output = values.get('output')
            for input in r_input:
                if input not in params.keys():
                    raise Exception('Input parameter %s doesnt exists' % input)

            for output in r_output:
                if output not in outputs.keys():
                    raise Exception('Output parameter %s doesnt exists' % output)
            if len(r_input) > 0:
                for param in params.keys():
                    if param not in r_input:
                        params.pop(param)
            if len(r_output) > 0:
                for output in outputs.keys():
                    if output not in r_output:
                        outputs.pop(output)
            template.append(generate_template(task_name, desc, params, outputs, service_name))
        final_template = create_template(template)
        return final_template
    except Exception as e:
        print e
        raise Exception("Error in Generating Template.\nReason")
