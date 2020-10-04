import setuptools

with open("README.md", "r") as fh:
  long_description = fh.read()

setuptools.setup(
  name="tflens-neovasili",
  version="0.0.1.dev1",
  author="Juan Manuel Ruiz Fernández",
  author_email="jruizferprofesional@gmail.com",
  description="Terraform state viewer",
  keywords="terraform viewer state tfstate cli",
  long_description=long_description,
  long_description_content_type="text/markdown",
  url="https://github.com/neovasili/tflens",
  packages=setuptools.find_packages(),
  entry_points = {
    "console_scripts": ['tflens = tflens.__main__:main']
  },
  classifiers=[
    "Development Status :: 3 - Alpha",
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