# -*- coding: utf-8 -*-
from setuptools import setup, find_packages

packages = find_packages(exclude=('readme_resource'))


def get_dis():
    with open("README.md", "r", encoding="utf-8") as f:
        return f.read()


def main():
    dis = get_dis()
    setup(
        name="nonebot-plugin-todo",
        version="0.1.3",
        url="https://github.com/CofinCup/nonebot_plugin_todo",
        packages=packages,
        keywords=["nonebot", "todo", "todo_list"],
        description="一款自动识别提醒内容并且可生成todo图片的nonebot插件",
        long_description_content_type="text/markdown",
        long_description=dis,
        author="CofinCup",
        author_email="864341840@qq.com",
        python_requires=">=3.9",
        license="MIT License",
        classifiers=[
            "Framework :: AsyncIO",
            "Operating System :: OS Independent",
            "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
            "Programming Language :: Python",
            "Programming Language :: Python :: 3.7",
            "Programming Language :: Python :: 3.8",
            "Programming Language :: Python :: 3.9",
            "Programming Language :: Python :: Implementation :: CPython"
        ],
        include_package_data=True
    )


if __name__ == "__main__":
    main()