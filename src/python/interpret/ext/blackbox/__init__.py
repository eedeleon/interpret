import logging
import pkg_resources
import sys

module_logger = logging.getLogger(__name__)

blackbox_key = "interpret_ext_blackbox"


def is_valid(ext_class):
    return True


for entrypoint in pkg_resources.iter_entry_points("interpret_ext_blackbox"):
    try:
        print(entrypoint.name, entrypoint.load())
        # How to get the current module
        # https://stackoverflow.com/questions/1676835
        current_module = sys.modules[__name__]
        blackbox_ext_class = entrypoint.load()

        if getattr(current_module, blackbox_ext_class.__name__, None) is None and is_valid(blackbox_ext_class):
            setattr(current_module, blackbox_ext_class.__name__,
                    blackbox_ext_class)

    except Exception as e:
        module_logger.warning("Failure while loading {}. Failed to load entrypoint {} with exception {}.".format(
            blackbox_key, entrypoint, e))
