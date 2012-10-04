from setuptools import setup, find_packages
import staticblog

setup(
    name = 'django-staticblog',
    version = staticblog.__version__,
    packages = find_packages(),
    requires = ['markdown', 'html2text'],
    author = 'Chris Grice',
    author_email = 'chris@chrisgrice.com',
    license = 'MIT',
    description = 'Markdown-based blog engine that compiles to static html pages',
    url='http://github.com/cgrice/django-staticblog/',
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
