import os
import subprocess
import glob

PYTHON_PROJECT = "./python/**"

def main():
    file_paths = [comp for comp in glob.glob(PYTHON_PROJECT, recursive=True) if os.path.isfile(comp) if comp.endswith("Dockerfile")]
    for file_path in file_paths[:2]:
        print(file_path)
        result = "./hadolint/{}".format(file_path[2:])
        command = "docker run --rm -i hadolint/hadolint hadolint - --format json < {} | jq .".format(file_path)
        try:
            res = subprocess.call(command.split())
        except Exception as e:
            print(e)


if __name__ == "__main__":
    main()