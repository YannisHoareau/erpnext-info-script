import sys
import json

ALLOWED_ARGS = ["-h", "--help", "-j", "--json"]

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
        # exit()

    res_array = dict()
    app_path = argv[-1]

    import frappe
    from frappe import cint

    res_sites = dict()

    for site in sorted(frappe.utils.get_sites()):
        res_sites[site] = dict()
        frappe.init(site)
        frappe.connect()
        res_sites[site]["schduler"] = True if cint(frappe.db.get_single_value("System Settings", "enable_scheduler")) == 1 else False
        res_sites[site]["maintenance"] = True if frappe.local.conf.maintenance_mode == 1 else False

    res_array["sites"] = res_sites

    res_apps = dict()

    for app in sorted(frappe.get_installed_apps()):
        res_apps[app] = dict()
        res_apps[app]["version"] = frappe.get_module(app).__version__

    res_array["apps"] = res_apps

    print(json.dumps(res_array, indent=4))
