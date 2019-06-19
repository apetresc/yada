"""
This module attempts to auto-detect your operating system and distribution
so that certain pieces of behaviour can be tuned appropriately.
"""

import platform


def enum(*sequential, **named):
    enums = dict(zip(sequential, range(len(sequential))), **named)
    reverse = dict((value, key) for key, value in enums.items())
    enums['reverse_mapping'] = reverse
    return type('Enum', (), enums)


Platform = enum('LINUX', 'OSX')

__PLATFORM_MAP = {
    'linux': Platform.LINUX,
    'darwin': Platform.OSX
}

UNIX_PLATFORMS = [Platform.LINUX, Platform.OSX]

CURRENT_PLATFORM = __PLATFORM_MAP[platform.system().lower()]

def platform_name(platform):
    return Platform.reverse_mapping[platform]


Distribution = enum('ARCH', 'UBUNTU')

__DISTRO_MAP = {
    'arch': Distribution.ARCH,
    'ubuntu': Distribution.UBUNTU
}

if CURRENT_PLATFORM == Platform.LINUX:
    CURRENT_DISTRO = __DISTRO_MAP[platform.linux_distribution()[0].lower()]
else:
    CURRENT_DISTRO = None
