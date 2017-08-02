import json
import sys
import copy
import traceback

if __name__ == "__main__":

    print('build from metric_service.json...')

    json_info_list = ['template', 'service', 'panel']
    info = {}

    try:
        for info_name in json_info_list:
            with open('./metric_%s.json' % (info_name), 'r') as f:
                info[info_name] = json.load(f)

        with open('./metric_option.json', 'r') as f:
            json_opts = f.read()

    except IOError:
        print('Exception: cannot open files')
        traceback.print_exc()

    for index in range(0, len(info['service']['services'])):
        serviceName = info['service']['services'][index]

        cur_json_opts = json_opts.replace('{service}', serviceName)
        opts = json.loads(cur_json_opts)

        panel = copy.deepcopy(info['panel'])

        for opt_id in opts.keys():
            opt_json_item = {}
            opt_json_item['refId'] = opt_id
            opt_json_item['target'] = opts[opt_id]

            panel['targets'].append(opt_json_item)

        panel['title'] = serviceName

        info['template']['rows'][0]['panels'].append(panel)

    with open('./metric_result.json', 'w') as f:
        f.write(json.dumps(info['template']))

    print('build success. open metric_result.json to view detail.')

    exit(0)
