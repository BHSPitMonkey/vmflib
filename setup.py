from setuptools import setup, find_packages

setup(
    name = "vmflib",
    version = "0.1",
    packages = find_packages(),
    scripts = ['tools/buildbsp.py'],

    entry_points = {
        'console_scripts': [
            'buildbsp = buildbsp:main'
        ]
    },

    # metadata for upload to PyPI
    author = "Stephen Eisenhauer",
    author_email = "bhs2007@gmail.com",
    description = "A package for creating Valve Map Format (VMF) files for the Source engine",
    license = "BSD",
    keywords = "vmf valve map format source engine",
    url = "http://github.com/BHSPitMonkey/vmflib", 
    # could also include long_description, download_url, classifiers, etc.
)
