import os
import subprocess

from setuptools import setup, find_packages


def parse_requirements(filename):
    with open(filename) as f:
        lines = f.read().splitlines()

    requires = []

    for line in lines:
        if "http" in line:
            pkg_name_without_url = line.split('@')[0].strip()
            requires.append(pkg_name_without_url)
        else:
            requires.append(line)

    return requires


def get_version():
    command = ["git", "describe", "--tags"]
    try:
        version = subprocess.check_output(command).decode().strip()
        version_parts = version.split("-")
        if len(version_parts) > 1 and version_parts[0].startswith("magic_pdf"):
            return version_parts[1]
        else:
            raise ValueError(f"Invalid version tag {version}. Expected format is magic_pdf-<version>-released.")
    except Exception as e:
        print(e)
        return "0.0.0"


def write_version_to_commons(version):
    commons_path = os.path.join(os.path.dirname(__file__), 'magic_pdf', 'libs', 'version.py')
    with open(commons_path, 'w') as f:
        f.write(f'__version__ = "{version}"\n')


if __name__ == '__main__':
    version_name = get_version()
    write_version_to_commons(version_name)
    setup(
        name="magic_pdf",  # 项目名
        version=version_name,  # 自动从tag中获取版本号
        packages=find_packages(),  # 包含所有的包
        install_requires=parse_requirements('requirements.txt'),  # 项目依赖的第三方库
        python_requires=">=3.9",  # 项目依赖的 Python 版本
        # entry_points={"console_scripts": ["my_command=my_project.main:run"]}, # 项目提供的可执行命令
        include_package_data=True,  # 是否包含非代码文件，如数据文件、配置文件等
        zip_safe=False,  # 是否使用 zip 文件格式打包，一般设为 False
    )
