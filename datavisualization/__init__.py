import os
import glob

# Get the directory of the current file
current_dir = os.path.dirname(__file__)

# Find all .py files in the directory except for __init__.py
modules = glob.glob(os.path.join(current_dir, "*.py"))

# Create a list of module names to be included in __all__
__all__ = [os.path.basename(f)[:-3] for f in modules if os.path.isfile(f) and not f.endswith('__init__.py')]

# Import all modules listed in __all__
for module in __all__:
    __import__(f"{__name__}.{module}")