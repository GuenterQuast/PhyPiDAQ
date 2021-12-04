"""
.. module:: _version_info
   :platform: python 2.7, 3.4
   :synopsis: Version 1.01b of phypidaq

.. moduleauthor:: Guenter Quast <guenter.quast@online.de>
"""

major = 1
minor = 0
revision = 1


def _get_version_tuple():
    """
version as a tuple
    """
    return (major, minor, revision)

def _get_version_string():
    """
  version as a string
    """
    return "%d.%d.%d" % _get_version_tuple()
