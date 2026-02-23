import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="transip-access-token-python",
    version="1.0.0",
    author="Rutger de Graaf",
    author_email="",
    description="TransIP Access Token Python library",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/rdegraafwhizzkit/transip-access-token",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.10',
    install_requires=[
        'requests',
        'cryptography'
    ]
)
