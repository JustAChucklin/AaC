# WARNIG - DO NOT EDIT - YOUR CHANGES WILL NOT BE PROTECTED
# This file is auto-generated by aac gen-plugin and may be overwritten.

from setuptools import setup
from aac_spec_impl import plugin_version

setup(
    version=plugin_version,
    name="aac-spec",
    install_requires=["aac"],
    entry_points={
        "aac": ["aac-spec=aac_spec"],
    },
)