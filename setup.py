from setuptools import setup, find_packages

install_requires = [
    'lxml>=4.5.0',
    'zope.interface>=4.1.3',
]

setup(
    name='cpcli',
    version='0.8',
    description='Competitive Programming CLI',
    author='Aditya Kumar',
    author_email='k.aditya00@gmail.com',
    long_description=open('README.rst', 'r', encoding='utf-8').read(),
    package_dir={'': 'src'},
    packages=find_packages(where='src', exclude=('tests', 'tests.*')),
    entry_points={'console_scripts': ['cpcli = cpcli.cmdline:execute']},
    python_requires='>=3.6',
    install_requires=install_requires,
    include_package_data=True,
    url='https://github.com/adityaa30/cpcli',
    download_url='https://github.com/adityaa30/cpcli/releases/tag/0.8',
    keywords=['CLI', 'Competitive Programming'],
    zip_safe=False,
    license='MIT License',
    classifiers=[
        'Topic :: Education',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
    ],
)
