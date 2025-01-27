"""Tools for handling plugin execution results consistently."""

from typing import Callable, Tuple, Any
from attr import attrib, attrs, validators, Factory
from contextlib import contextmanager
from enum import Enum, auto, unique
from traceback import extract_tb

from aac.io.parser import ParserError
from aac.plugins import PluginError, OperationCancelled
from aac.validate import ValidationError


@unique
class PluginExecutionStatusCode(Enum):
    """An enumeration that represents status codes for plugins to return."""

    SUCCESS = 0
    VALIDATION_FAILURE = auto()
    PARSER_FAILURE = auto()
    PLUGIN_FAILURE = auto()
    OPERATION_CANCELLED = auto()
    GENERAL_FAILURE = auto()


@attrs(slots=True, auto_attribs=True)
class PluginExecutionResult:
    """Provides information regarding the results of the execution of a plugin.

    Attributes:
        name (str): The name of the plugin whose results are included.
        status_code (PluginExecutionStatusCode): A status code for the plugin execution.
        messages (list[str]): A list of messages for the user.
    """

    name: str = attrib(validator=validators.instance_of(str))
    status_code: PluginExecutionStatusCode = attrib(
        validator=validators.instance_of(PluginExecutionStatusCode)
    )
    messages: list[str] = attrib(
        default=Factory(list), validator=validators.instance_of(list)
    )

    def add_messages(self, *messages) -> None:
        """Add messages to the list of messages."""
        self.messages.extend(messages)

    def set_messages(self, *messages) -> None:
        """Clear the current messages and set them to the passed in messages."""
        self.messages = list(messages)

    def is_success(self) -> bool:
        """Return True if the command succeeded; False, otherwise."""
        return self.status_code == PluginExecutionStatusCode.SUCCESS

    def get_messages_as_string(self) -> str:
        """Return the output messages as a combined string."""
        return "\n".join(self.messages)


@contextmanager
def plugin_result(name: str, cmd: Callable, *args: Tuple[Any], **kwargs: dict[str, Any]):
    """
    Create a PluginExecutionResult after running command on a validated model from file.

    This context manager will yield the validation result containing the valid model contained in
    the provided architecture file. If the model is invalid or the file doesn't exist, nothing will
    be yielded and the result will be returned.

    Arguments:
        name (str): The name of the plugin whose result is being returned.
        cmd (str): The command to be called. The command is expected to return a message to be
                       displayed to the user.
        args (Tuple[Any]): a list of args that are passed to the accompanying command
        kwargs (dict[str, Any]): a dictionary of keyword arguments that are passed to the accompanying command

    Yields:
        A PluginExecutionResult populated with any errors that might have been encountered.
    """
    result = PluginExecutionResult(name, PluginExecutionStatusCode.SUCCESS)
    try:
        result.add_messages(cmd(*args, **kwargs))
    except ParserError as error:
        source, errors = error.args
        result.add_messages(f"Failed to parse {source}\n", *errors, "")
        result.status_code = PluginExecutionStatusCode.PARSER_FAILURE
    except ValidationError as error:
        result.add_messages("Failed to validate:\n", *error.args, "")
        result.status_code = PluginExecutionStatusCode.VALIDATION_FAILURE
    except FileNotFoundError as error:
        result.add_messages(f"{error.strerror}: {error.filename}")
        result.status_code = PluginExecutionStatusCode.GENERAL_FAILURE
    except PluginError as error:
        result.set_messages(error.message)
        result.status_code = PluginExecutionStatusCode.PLUGIN_FAILURE
    except OperationCancelled as condition:
        result.set_messages(condition.message)
        result.status_code = PluginExecutionStatusCode.OPERATION_CANCELLED
    except Exception as error:
        # Extract the first stack trace, skipping the plugin result we'd expect to find in the first element
        error_trace = extract_tb(error.__traceback__)[1]
        result.add_messages(
            f"An unrecognized error occurred:{error_trace.filename} line {error_trace.lineno} message: {error}"
        )
        result.status_code = PluginExecutionStatusCode.GENERAL_FAILURE

    yield result
