def generate_tasks(task_name, params, outputs, service_name):
    task_input = dict()
    task_publish = dict()
    for param in params.keys():
        v = "<%% $.%s %%>" % param
        task_input.update({param: v})
    for key, value in outputs.items():
        v = "<%% $.%s.%s %%>" % (task_name, key)
        task_publish.update({key: v})
    task_detail = {
        'action': str("%s.%s") % (service_name.lower(), task_name),
        'description': task_name,
        'use_swagger': True,
    }
    if task_input:
        task_detail.update({'input': task_input})
    if task_publish:
        task_detail.update({'publish': task_publish})
    return {task_name: task_detail}


def generate_workflow(task, desc, inputs, tasks, outputs):
    task_output = dict()
    for key, value in outputs.items():
        v = "<%% $.%s.%s %%>" % (task, key)
        task_output.update({key: v})
    template = {
        'version': "2.0",
        task: {
            'type': 'direct',
            'description': desc,
            'tasks': tasks
            }
        }
    if inputs:
        template[task]['input'] = inputs
    if task_output:
        template[task]['output'] = task_output
    return template


def generate_template(task_name, desc, inputs, outputs, service_name):
    tasks = generate_tasks(task_name, inputs, outputs, service_name)
    template = generate_workflow(task_name, desc, inputs, tasks, outputs)
    return template


def create_template(template_list):
    inputs = dict()
    outputs = dict()
    tasks = dict()
    workflow_name = 'workflow'
    desc = ''
    for template in template_list:
        wf_name = ''
        wf_dict = dict()
        for k, v in template.items():
            if k == 'version':
                continue
            else:
                wf_name = k
                wf_dict = v
        if 'input' in wf_dict:
            inputs.update(wf_dict.get('input'))
        if 'output' in wf_dict:
            outputs.update(wf_dict.get('output'))
        tasks.update(wf_dict.get('tasks'))
        workflow_name = "%s_%s" % (workflow_name, wf_name)
        desc = "%s %s" % (desc, wf_dict.get('description'))
    final_template = {
        'version': '2.0',
        workflow_name: {
            'type': 'direct',
            'description': desc,
            'tasks': tasks
        }
    }
    if inputs:
        final_template[workflow_name].update({'input': inputs})
    if outputs:
        final_template[workflow_name].update({'output': outputs})
    return final_template
