import setuptools

setuptools.setup(
    name="nfc_attendance",
    packages=setuptools.find_packages("."),
    install_requires=[
        "sqlalchemy",
        "fastapi[all]"
    ]
)
