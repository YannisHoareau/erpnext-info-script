import sys
import json
import os

ALLOWED_ARGS = ["-h", "--help", "-j", "--json"]

def check_path(files_path):
    if not files_path.endswith('/'):
        files_path += '/'
    return files_path + 'development/frappe-bench/sites/'

if __name__ == 'erpnext_info':
    argv = sys.argv[1:]
    args = argv[1:-1]

    unallowed_arg = False

    for arg in args:
        if arg not in ALLOWED_ARGS:
            unallowed_arg = True

    if "-h" in args or "--help" in args or unallowed_arg:
        print('''
        Usage: python3 erpnext-info.py [OPTIONS] ERPNEXT_PATH
            -j, --json: Outputs json in cli.
            -h, --help: This usage screen.
        '''.strip())
        exit()

    res_array = dict()
    app_path = argv[-1]
    files_path = check_path(app_path)

    try:
        with open(files_path + 'apps.json') as f:
            json_apps = json.load(f)
    except FileNotFoundError:
        print('Bad path provided')
        exit()

    apps = dict()
    for app in json_apps:
        apps[app] = json_apps[app]["version"]

    res_array["apps"] = apps

    sites = dict()
    for dir in os.listdir(files_path):
        dir_path = os.path.join(files_path, dir)
        if os.path.isdir(dir_path) and 'site_config.json' in os.listdir(dir_path):
            sites[dir] = dict()

    res_array["sites"] = sites

    print(json.dumps(res_array, indent=4))
