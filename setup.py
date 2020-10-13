import setuptools

with open("README.md", "r") as fh:
  long_description = fh.read()

setuptools.setup(
  name="tflens",
  version="1.0.1",
  author="Juan Manuel Ruiz Fernández",
  description="Terraform state viewer",
  keywords="terraform viewer state tfstate cli",
  long_description=long_description,
  long_description_content_type="text/markdown",
  url="https://github.com/neovasili/tflens",
  packages=setuptools.find_packages(include=[
    'tflens',
    'tflens.controller',
    'tflens.exception',
    'tflens.helper',
    'tflens.model',
    'tflens.service'
  ]),
  entry_points = {
    "console_scripts": ['tflens = tflens.__main__:main']
  },
  classifiers=[
    "Development Status :: 5 - Production/Stable",
    "Environment :: Console",
    "Intended Audience :: Developers",
    "License :: OSI Approved :: MIT License",
    "Natural Language :: English",
    "Operating System :: OS Independent",
    "Programming Language :: Python :: 3",
    "Topic :: Software Development :: Documentation",
    "Topic :: Terminals",
  ],
  python_requires='>=3.6',
)
