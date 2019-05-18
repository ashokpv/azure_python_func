from constants import base_template_action_id
from constants import EXCLUDE_OUTPUT_PARAMS
from constants import EXCLUDE_INPUT_PARAMS
from constants import success_resp


def get_details(swagger_schema, operation_id):
    global_params_dict = swagger_schema.get('parameters')
    global_params = list()
    params = list()
    task_name = outputs = desc = None
    if global_params_dict:
        for k, v in global_params_dict.items():
            global_params.append(v)
    for key, value in swagger_schema.get('paths').items():
        for http_method in value.keys():
            api_dict = value.get(http_method)
            if isinstance(api_dict, dict) and api_dict.get('operationId') == operation_id:
                desc = api_dict.get('description')
                outputs = parse_output(swagger_schema, api_dict.get('responses'))
                params = api_dict.get('parameters')
                task_name = str(api_dict.get(base_template_action_id))
    if not task_name:
        raise Exception('Please verify OperationId %s' % operation_id)
    for param in params:
        global_params.append(param)
    inputs = generate_params(swagger_schema, global_params)
    return str(task_name), desc, inputs, outputs


def generate_params(swagger_schema, params):
    inputs = dict()
    for param in params:
        task_input = param.get('name')
        if not task_input or task_input in EXCLUDE_INPUT_PARAMS:
            continue
        param_recursive(swagger_schema, param, inputs)
    for k, v in inputs.items():
        if k == 'None':
            inputs.pop(k)
    return inputs


def param_recursive(swagger_schema, param, inputs):
    ref_object, def_name = is_schema(param)
    if ref_object:
        param_def = swagger_schema.get('definitions').get(def_name)
        if param_def.get('properties'):
            for prop, value in param_def.get('properties').items():
                if not is_schema(value)[0]:
                    input_details = {
                        'type': str(value.get('type', 'string')),
                        'description': str(value.get('description', ''))
                    }
                    in_dict = {str(prop): input_details}
                    inputs.update(in_dict)
                param_recursive(swagger_schema, value, inputs)
    else:
        input_details = {
            'type': str(param.get('type', 'string')),
            'description': str(param.get('description', ''))
        }
        inputs.update({str(param.get('name')): input_details})
    return inputs


def parse_output(swagger_schema, responses):
    outputs = dict()
    for resp in responses.keys():
        if resp not in success_resp:
            responses.pop(resp)
    for resp, value in responses.items():
        output_recursive(swagger_schema, value, outputs)
    for output in outputs.keys():
        if output == 'None':
            outputs.pop(output)
    return outputs


def output_recursive(swagger_schema, param, outputs):
    ref_object, def_name = is_schema(param)
    if ref_object:
        param_def = swagger_schema.get('definitions').get(def_name)
        if param_def.get('properties'):
            for prop, value in param_def.get('properties').items():
                if not is_schema(value)[0]:
                    outputs.update({str(prop): str(prop)})
            if prop not in EXCLUDE_OUTPUT_PARAMS:
                param_recursive(swagger_schema, value, outputs)
    return outputs


def is_schema(param):
    if param.get('schema'):
        return True, param.get('schema').get('$ref').split('/')[-1]
    elif param.get('$ref'):
        return True, param.get('$ref').split('/')[-1]
    return False, None
