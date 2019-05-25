from setuptools import setup, find_packages
from yada import __VERSION__

setup(
    name='yada',
    version=__VERSION__,
    packages=find_packages(),
    url='https://github.com/apetresc/yada',
    author='Adrian Petrescu',
    author_email='adrian@apetre.sc',
    description='Yet another dotfile aggregator',

    install_requires=[
        'Click==7.0',
        'Jinja2==2.10.1',
        'MarkupSafe==0.23',
        'pexpect==3.2',
        'clint==0.3.7',
        'coloured_text==2.0'
    ],

    entry_points='''
        [console_scripts]
        yada=yada.cli.main:cli
    '''
)
