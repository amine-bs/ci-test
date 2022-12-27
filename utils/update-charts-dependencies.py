import yaml
import os
from pathlib import Path
import traceback

def update_chart(path):
    chart_yaml_path = os.path.join(path, 'Chart.yaml')
    with open(chart_yaml_path) as f:
        chart = yaml.safe_load(f)
    increment_version = False
    dependencies = chart["dependencies"]
    new_dependencies = []
    for dependency in dependencies:
        name = dependency["name"]
        version = dependency["version"]
        os.system("helm repo add {} {}".format(name, dependency["repository"]))
        os.system("helm show chart {}/{} > {}.yaml".format(name, name, name))
        with open("{}.yaml".format(name)) as f:
            dependency_chart = yaml.safe_load(f)
        os.system("rm {}.yaml".format(name))
        latest_version = dependency_chart["version"]
        if version != latest_version:
            increment_version = True
        dependency["version"] = latest_version
        new_dependencies.append(dependency)
    chart["dependencies"] = new_dependencies
    if increment_version:
        print("updates found..")
        chart_old_version = chart["version"]
        chart_new_version = "{}.{}.{}".format(chart_old_version.split(".")[0], chart_old_version.split(".")[1], str(int(chart_old_version.split(".")[2])+1))
        chart["version"] = chart_new_version
        with open(chart_yaml_path, 'w') as f:
            yaml.dump(chart, f)
        print("update done!")

if __name__ == "__main__":
   paths = Path("charts")
   for path in paths.iterdir():
       try:
           update_chart(str(path.absolute()))
       except Exception as e:
           print(f"Failed processing chart {path}")
           print(traceback.format_exc())

