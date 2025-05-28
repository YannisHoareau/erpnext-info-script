import sys

ALLOWED_ARGS = ["-h", "--help", "-j", "--json"]

def create_info_dict(site_list, app_list):
	res = dict()
	res_sites = dict()
	res_apps = dict()

	for site in sorted(site_list):
		res_sites[site] = dict()
		frappe.init(site)
		frappe.connect()
		res_sites[site]["scheduler"] = True if cint(frappe.db.get_single_value("System Settings", "enable_scheduler")) == 1 else False
		res_sites[site]["maintenance"] = True if frappe.local.conf.maintenance_mode == 1 else False
		res_sites[site]["url"] = get_url()

	for app in app_list:
		res_apps[app] = {
			"app_version": frappe.get_module(app).__version__ or "UNVERSIONED"
		}

	res["sites"] = res_sites
	res["apps"] = res_apps
	return res

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
		exit(1)

	try:
		import os
		import frappe
		from frappe import cint, get_all_apps
		from frappe.utils import get_sites, get_url
	except ImportError:
		exit(1)

	bench_path = argv[-1]
	old_cwd = os.getcwd()
	sites_path = os.path.join(bench_path, "sites")
	os.chdir(sites_path)

	res_array = create_info_dict(get_sites(), get_all_apps(with_internal_apps=False, sites_path=sites_path))

	if print_json:
		import json
		print(json.dumps(res_array, indent=2))
		os.chdir(old_cwd)
		exit(0)

	os.chdir(old_cwd)
	exit()
else:
	try:
		import frappe
		from frappe import cint
		from frappe.utils import get_url
	except ImportError:
		exit(1)
