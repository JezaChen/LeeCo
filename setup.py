from setuptools import find_packages, setup


def get_description():
    with open("README.md") as file:
        return file.read()


setup(
    name="LeeCo",
    version="0.0.1a0",
    url="https://github.com/JezaChen/LeeCo",
    author="Jianzhang Chen",
    author_email="jezachen@163.com",
    license="MIT",
    description="LeeCo: A utility for empowering the local debugging of LeetCode problems with testcases.",
    long_description=get_description(),
    long_description_content_type="text/markdown",
    packages=find_packages(exclude=("*examples", "*examples.*")),
    python_requires=">=3.7, <4",
    keywords="leetcode",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Operating System :: Microsoft :: Windows",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Development Status :: 4 - Beta",
        "License :: OSI Approved :: MIT License",
    ],
    package_data={
        'leeco': ['*.pyi', 'py.typed'],
    }
)
