"""AaC Plugin implementation module for the report plugin."""
# NOTE: It is safe to edit this file.
# This file is only initially generated by the aac gen-plugin, and it won't be overwritten if the file already exists.

from aac.plugins.plugin_execution import PluginExecutionResult, plugin_result

plugin_name = "report"


def report(report_definition_file: str, architecture_file: str, output_file: str) -> PluginExecutionResult:
    """
    Generate YAML output from an Arch-as-Code report definition.

    Args:
        report_definition_file (str): The yaml file containing the report model.
        architecture_file (str): The yaml file containing the AaC model to interrogate.
        output_file (str): The file to write the generated YAML report. (Optional)
    """
    # TODO add implementation here
    def _implement_and_rename_me():
        raise NotImplementedError("report is not implemented.")

    with plugin_result(plugin_name, _implement_and_rename_me) as result:
        return result


def report_csv(report_definition_file: str, architecture_file: str, output_file: str) -> PluginExecutionResult:
    """
    Generate CSV output from an Arch-as-Code report definition.

    Args:
        report_definition_file (str): The yaml file containing the report model.
        architecture_file (str): The yaml file containing the AaC model to interrogate.
        output_file (str): The file to write the generated CSV report. (Optional)
    """
    # TODO add implementation here
    def _implement_and_rename_me():
        raise NotImplementedError("report_csv is not implemented.")

    with plugin_result(plugin_name, _implement_and_rename_me) as result:
        return result
