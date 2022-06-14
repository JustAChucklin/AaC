"""AaC Plugin implementation module for the aac-rest-api plugin."""
# NOTE: It is safe to edit this file.
# This file is only initially generated by the aac gen-plugin, and it won't be overwritten if the file already exists.

from fastapi.openapi.utils import get_openapi
from typing import Optional
import json
import os
import uvicorn

from aac.plugins.plugin_execution import PluginExecutionResult, plugin_result
from aac.plugins.rest_api.aac_rest_app import app

plugin_name = "aac-rest-api"


def rest_api(host: Optional[str], port: Optional[int]) -> PluginExecutionResult:
    """
    Start a RESTful interface for interacting with and managing AaC.

    Args:
        host (Optional[str]): Set the hostname of the service. Useful for operating behind proxies.
        port (Optional[int]): The port to which the RESTful service will be bound.
    """
    with plugin_result(plugin_name, _start_restful_service, host, port) as result:
        return result


def _start_restful_service(host: Optional[str] = "0.0.0.0", port: Optional[int] = 8000) -> str:
    """Start the RESTful interface service."""
    uvicorn.run(app, host=host, port=port)
    return "Successfully started and stopped the RESTful API."


def generate_api_spec(output_directory: str) -> None:
    """
    Write the OpenAPI schema to a JSON file.

    Args:
        output_directory (str): The output directory in which to write the AaC OpenAPI JSON file.
    """
    with plugin_result(plugin_name, _write_openapi_spec_to_file, output_directory) as result:
        return result


def _write_openapi_spec_to_file(output_directory: str) -> str:
    full_file_path = os.path.join(output_directory, "AaC_OpenAPI_Schema.json")

    with open(full_file_path, "w") as output_file:
        json.dump(
            get_openapi(
                title=app.title,
                version=app.version,
                openapi_version=app.openapi_version,
                description=app.description,
                routes=app.routes,
            ),
            output_file,
        )

    return f"Successfully wrote the OpenAPI spec to {full_file_path}."