"""Setup.py module for the aac-gen-protobuf plugin."""
# WARNING - DO NOT EDIT - YOUR CHANGES WILL NOT BE PROTECTED.
# This file is auto-generated by the aac gen-plugin and may be overwritten.

from setuptools import setup
from aac_gen_protobuf_impl import plugin_version

setup(
    version=plugin_version,
    name="aac-gen-protobuf",
    install_requires=["aac"],
    entry_points={
        "aac": ["aac-gen-protobuf=aac_gen_protobuf"],
    }
)
