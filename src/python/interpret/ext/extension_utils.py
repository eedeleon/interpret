import logging
import pkg_resources
import re
import sys

module_logger = logging.getLogger(__name__)

blackbox_key = "interpret_ext_blackbox"


def _validate_class_name(proposed_class_name):
    # regex for class name came from
    # https://stackoverflow.com/questions/10120295
    match = re.match(r"[a-zA-Z_][a-zA-Z_0-9]+", proposed_class_name)
    if match is None:
        raise ValueError("Invalid class name {}. Class names must start with a "
                         " letter or underscore. And can continue with letters, underscores, and integers")


def load_class_extensions(current_module, extension_key, extension_class_validator, current_module_all):
    for entrypoint in pkg_resources.iter_entry_points(extension_key):
        try:
            extension_class_name = entrypoint.name
            _validate_class_name(extension_class_name)
            extension_class = entrypoint.load()
            module_logger.debug("loading entrypoint key {} with name {} with object {}".format(
                extension_key, extension_class_name, extension_class))

            if getattr(current_module, extension_class_name, None) is None and \
               extension_class_validator(extension_class):
                setattr(current_module, extension_class_name, extension_class)
                current_module_all.append(extension_class_name)

        except Exception as e:
            module_logger.warning("Failure while loading {}. Failed to load entrypoint {} with exception {}.".format(
                blackbox_key, entrypoint, e))
