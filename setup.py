import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="emitter-io",
    version="2.0.1",
    author="Florimond Husquinet",
    author_email="florimond@emitter.io",
    description="A Python library to interact with the Emitter API.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://emitter.io",
    packages=["emitter"],
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "Topic :: Communications",
        "Topic :: Internet :: WWW/HTTP",
        "License :: OSI Approved :: Eclipse Public License 1.0 (EPL-1.0)",
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 3"
    ],
    keywords="emitter mqtt realtime cloud service",
    install_requires=["paho-mqtt"]
)
