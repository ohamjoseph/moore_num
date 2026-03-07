from setuptools import setup, find_packages
import os

def read_readme():
    with open(os.path.join(os.path.dirname(__file__), "README.md"), encoding="utf-8") as f:
        return f.read()

setup(
    name="moore_num",
    version="0.1.2",
    packages=find_packages(),
    entry_points={
        "console_scripts": [
            "num2moore=moore_num.cli:main",
        ],
    },
    author="Hamed",
    author_email="hamed.ouily@gmail.com",
    description="A library to convert numbers to Mooré text and vice versa",
    long_description=read_readme(),
    long_description_content_type="text/markdown",
    url="https://github.com/ohamjoseph/moore_num.git",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Development Status :: 4 - Beta",
        "Topic :: Text Processing :: Linguistic",
    ],
    python_requires=">=3.6",
    keywords="moore, language, mossi, numbers, conversion, burkina faso",
)
