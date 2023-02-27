import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="bilifm",
    version="0.1.5",
    author="Felix Jing",
    author_email="jingfelix@outlook.com",
    description="Download Bilibili videos as audios.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/jingfelix/bilifm",
    project_urls={
        "Bug Tracker": "https://github.com/jingfelix/bilifm/issues",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Operating System :: OS Independent",
    ],
    entry_points={
        "console_scripts": ["bilifm=bilifm.__init__:app"],
    },
    install_requires=[
        "requests",
        "click",
        "typer",
        "rich",
    ],
    package_dir={"": "src"},
    packages=setuptools.find_packages(where="src"),
    python_requires=">=3.5",
)
