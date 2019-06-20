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
        'pytest-runner',
        'setuptools_scm'
    ],
    install_requires=[
        'Click==7.0',
        'click-pathlib==2019.6.13.1',
        'xdg==4.0.0',
    ],
    tests_require=[
        'pytest'
    ],

    entry_points='''
        [console_scripts]
        yada=yada.cli.main:cli
    '''
)
