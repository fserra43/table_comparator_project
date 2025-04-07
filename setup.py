from setuptools import setup, find_packages

setup(
    name="python_table_comparator",
    version="0.1",
    packages=find_packages(),
    description="Robust Python Table Comparator for DataFrames – a tool that validates primary keys (existence, uniqueness, column alignment), " \
    "compares rows and columns to identify discrepancies, and exports detailed multi-sheet Excel reports.",
    author="Your Name",
    author_email="fserrabisquerra@gmail.com",
    install_requires=[
        "pandas",
        "xlsxwriter",
        "seaborn",
    ],
)
