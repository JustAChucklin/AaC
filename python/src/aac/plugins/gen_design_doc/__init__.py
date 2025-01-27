"""The gen-design-doc plugin module."""
# NOTE: It is safe to edit this file.
# This file is only initially generated by aac gen-plugin, and it won't be overwritten if the file already exists.

from aac.cli.aac_command import AacCommand, AacCommandArgument
from aac.package_resources import get_resource_file_contents, get_resource_file_path
from aac.io.parser import parse
from aac.plugins import hookimpl
from aac.plugins.gen_design_doc.gen_design_doc_impl import gen_design_doc
from aac.plugins.plugin import Plugin

plugin_resource_file_args = (__package__, "gen_design_doc.yaml")


@hookimpl
def get_commands() -> list[AacCommand]:
    """
    Return a list of AacCommands provided by the plugin to register for use.

    This function is automatically generated. Do not edit.

    Returns:
        list of AacCommands
    """
    gen_design_doc_arguments = [
        AacCommandArgument(
            "architecture_files",
            "A comma-separated list of yaml file(s) containing the modeled system for which to generate the System Design document.",
        ),
        AacCommandArgument(
            "output_directory",
            "The directory to which the System Design document will be written.",
        ),
        AacCommandArgument(
            "--template_file",
            "The name of the Jinja2 template file to use for generating the document. (optional)",
        ),
    ]

    plugin_commands = [
        AacCommand(
            "gen-design-doc",
            "Generate a System Design Document from Architecture-as-Code models.",
            gen_design_doc,
            gen_design_doc_arguments,
        ),
    ]

    return plugin_commands


@hookimpl
def get_plugin_aac_definitions() -> str:
    """
    Return the plugin's AaC definitions.

    Returns:
         string representing yaml extensions and definitions defined by the plugin
    """
    return get_resource_file_contents(*plugin_resource_file_args)


@hookimpl
def get_plugin() -> Plugin:
    """
    Returns information about the plugin.

    Returns:
        A collection of information about the plugin and what it contributes.
    """
    plugin_definitions = parse(
        get_plugin_aac_definitions(),
        get_resource_file_path(*plugin_resource_file_args)
    )

    *_, plugin_name = __package__.split(".")
    plugin = Plugin(plugin_name)
    plugin.register_commands(get_commands())
    plugin.register_definitions(plugin_definitions)

    return plugin
