import sys

ALLOWED_ARGS = ["-h", "--help", "-j", "--json"]

if __name__ == '__main__':
	argv = sys.argv[1:]
	args = argv[:-1]

	unallowed_arg = False
	print_json = False

	for arg in args:
		if arg in ["-j", "--json"]:
			print_json = True
		if arg not in ALLOWED_ARGS:
			unallowed_arg = True

	if "-h" in args or "--help" in args or unallowed_arg:
		print('''
        Usage: python3 erpnext-info.py [OPTIONS] ERPNEXT_PATH
            -j, --json: Outputs json in cli.
            -h, --help: This usage screen.
        '''.strip())
		exit()

	try:
		import os
		import frappe
		from frappe import cint
		from frappe.utils import get_sites, get_installed_apps_info, get_url
	except ImportError:
		print("Error while importing frappe. Please check your installation.")
		exit()

	res_array = dict()
	bench_path = argv[-1]
	old_cwd = os.getcwd()

	os.chdir(os.path.join(bench_path, "sites"))

	res_sites = dict()

	for site in sorted(get_sites()):
		res_sites[site] = dict()
		frappe.init(site)
		frappe.connect()
		res_sites[site]["scheduler"] = True if cint(frappe.db.get_single_value("System Settings", "enable_scheduler")) == 1 else False
		res_sites[site]["maintenance"] = True if frappe.local.conf.maintenance_mode == 1 else False
		res_sites[site]["url"] = get_url()

	res_array["sites"] = res_sites

	res_apps = dict()

	for app in get_installed_apps_info():
		res_apps[app.get("app_name")] = {
			"app_version": app.get("version") or "UNVERSIONED"
		}

	res_array["apps"] = res_apps

	if print_json:
		import json
		print(json.dumps(res_array, indent=4))
	os.chdir(old_cwd)
	exit()
