import setuptools

with open("README.md", "r") as f:
    long_description = f.read()

with open('requirements.txt') as f:
    requirements = f.read().splitlines()

setuptools.setup(
    name='funkapi',
    version='0.1.5',
    install_requires=requirements,
    license='MIT License',
    author='Tim-Luca Lagmöller',
    author_email='hello@lagmoellertim.de',
    description='Reverse engineered API of Freenet FUNK',
    long_description=long_description,
    long_description_content_type="text/markdown",
    url='https://github.com/lagmoellertim/freenet-funk-api',
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
