from distutils.core import setup

setup (
    name="com.castsoftware.uc.action-plan",
    version="0.1.0",
    author="Nevin Kaplan",
    author_email="n.kaplan@castsoftware.com",
    url="https://github.com/CAST-Extend/com.castsoftware.uc.action-plan",
    packages=["cast_action_plan"],
    install_requires=['com.castsoftware.uc.python.common>=0.1','openpyxl','pandas','psycopg2'],
    package_data={'':['rules.xlsx']},
    include_package_data=True
)
