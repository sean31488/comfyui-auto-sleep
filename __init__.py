import logging
import sys

# Hibernate uses the Windows power API; elsewhere load neither the backend nor the button.
if sys.platform == "win32":
    from . import sleep_backend
    WEB_DIRECTORY = "./js"
else:
    logging.info("[AutoSleep] Windows only, disabled.")

NODE_CLASS_MAPPINGS = {}
__all__ = ["NODE_CLASS_MAPPINGS"]
