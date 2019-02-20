import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="mailpipe",
    version="0.0.1",
    author="Timothy Watts",
    author_email="tim@readevalprint.com",
    description="Django app to recieve emails directly to your project",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/readevalprint/mailpipe-app",
    packages=setuptools.find_packages(),
    classifiers=[
        "email", "django", "api"
    ],
)

