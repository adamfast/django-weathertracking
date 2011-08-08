from distutils.core import setup

setup(
    name = "django-weathertracking",
    url = "http://github.com/adamfast/django-weathertracking",
    author = "Adam Fast",
    author_email = "adamfast@gmail.com",
    version = "0.1",
    license = "BSD",
    packages = ["weathertracking"],
    install_requires = ['python-dateutil'],
    description = "App for getting current conditions.",
    classifiers = [
        "Programming Language :: Python",
        "Operating System :: OS Independent",
        "Topic :: Software Development",
        "Environment :: Web Environment",
        "Framework :: Django",
    ],
)
