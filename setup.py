from setuptools import setup, find_packages

setup(
    name="syncdb",
    version="1.0.0",
    description="A simple database schema synchronization tool",
    author="ObjectOriented0",
    packages=find_packages(),
    install_requires=[
        "sqlalchemy>=2.0.0",
        "psycopg2-binary>=2.9.0", 
        "mysql-connector-python>=8.0.0",
        "click>=8.0.0",
        "pyyaml>=6.0.0",
    ],
    entry_points={
        "console_scripts": [
            "syncdb=syncdb.cli:main",
        ],
    },
    python_requires=">=3.8",
)