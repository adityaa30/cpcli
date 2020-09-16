from setuptools import setup

install_requires = [
    'lxml>=4.5.0',
    'zope.interface>=4.1.3',
]

setup(
    name='cp-cli',
    version='0.1',
    description='Competitive Programming CLI',
    author='Aditya Kumar',
    author_email='k.aditya00@gmail.com',
    long_description=open('README.md', 'r', encoding='utf-8').read(),
    package_dir={'': 'src'},
    entry_points={'console_scripts': ['cpcli=cpcli.cmdline:execute']},
    python_requires='>=3.6',
    install_requires=install_requires,
    url='https://github.com/adityaa30/cp-cli',
    zip_safe=False,
    license='MIT License'
)
