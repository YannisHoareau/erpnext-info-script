import os
import sys
import json

ALLOWED_ARGS = ["-h", "--help", "-j", "--json"]

if __name__ == '__main__':
	argv = sys.argv[1:]
	args = argv[:-1]

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

	from bench.bench import Bench
	from bench.utils.app import get_current_version

	old_cwd = os.getcwd()
	bench_path = argv[-1]
	os.chdir(bench_path)
	res_array = dict()

	working_bench = Bench(bench_path)

	site_list = working_bench.sites
	app_list = working_bench.get_installed_apps()

	res_sites = dict()

	# Next commented part is old implem deprecated now
	# for site in sorted(frappe.utils.get_sites()):
	#     res_sites[site] = dict()
	#     frappe.init(site)
	#     frappe.connect()
	#     res_sites[site]["scheduler"] = True if cint(frappe.db.get_single_value("System Settings", "enable_scheduler")) == 1 else False
	#     res_sites[site]["maintenance"] = True if frappe.local.conf.maintenance_mode == 1 else False
	#     res_sites[site]["url"] = frappe.utils.get_url()

	# res_array["sites"] = res_sites

	res_apps = dict()

	for app_name in app_list:
		res_apps[app_name] = dict()
		app_version = get_current_version(app_name, bench_path=working_bench.name)
		res_apps[app_name]["version"] = app_version

	res_array["apps"] = res_apps

	print(json.dumps(res_array, indent=4))
	os.chdir(old_cwd)
	exit()
