from setuptools import setup, find_packages

with open("requirements.txt") as f:
    install_requires = f.read().strip().split("\n")

setup(
    name="frappe_pharmacy_batch_expiry_tracker",
    version="1.0.0",
    description="Frappe Pharmacy Batch Expiry Tracker - Official Frappe App & ERPNext Integration",
    author="Shyamkumar Pandey",
    author_email="shyampandey1104@gmail.com",
    packages=find_packages(),
    zip_safe=False,
    include_package_data=True,
    install_requires=install_requires
)
