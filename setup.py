from setuptools import setup, find_packages
import staticblog

setup(
    name = 'django-staticblog',
    version = staticblog.__version__,
    packages = find_packages(),
    install_requires = ['Markdown >= 2.0', 'html2text >= 3.0'],
    author = 'Chris Grice',
    author_email = 'chris@chrisgrice.com',
    license = 'MIT',
    description = 'Markdown-based blog engine that compiles to static html pages',
    url='http://github.com/cgrice/django-staticblog/',
    package_data = { 'django-staticblog': ['templates/*'] },
    classifiers = [
        'Development Status :: 3 - Alpha',
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Framework :: Django',
    ],
    zip_safe = False,
)
