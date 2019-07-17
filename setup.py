from setuptools import setup, find_packages

setup(
    name='yada',
    use_scm_version=True,
    packages=find_packages('src'),
    package_dir={'': 'src'},
    url='https://github.com/apetresc/yada',
    author='Adrian Petrescu',
    author_email='adrian@apetre.sc',
    description='Yet another dotfile aggregator',

    setup_requires=[
        'pytest-runner==5.1',
        'setuptools_scm==3.3.3'
    ],
    install_requires=[
        'Click>=7.0,<8.0',
        'pathlib2==2.3.3;python_version<"3.4"',
        'pyyaml>=5.1,<6.0'
    ],
    tests_require=[
        'pytest==4.6.3',
        'pyfakefs==3.6',
        'tox==3.12.1'
    ],
    package_data={'yada.data': ['config.yaml']},

    entry_points='''
        [console_scripts]
        yada=yada.cli.main:cli
    '''
)
