import importlib
import pkgutil


def load_models(package_name: str) -> None:
    """
    Dynamically loads all modules in a given package.

    This function imports all non-package modules within the specified package, ensuring
    that their contents (e.g., class definitions, functions) are loaded into memory. This is
    useful for dynamically registering models, configurations, or other resources during runtime.

    Args:
        package_name (str): The name of the package to load modules from.

    Usage:
        # Assuming the package structure:
        # my_package/
        # ├── __init__.py
        # ├── module1.py
        # └── module2.py
        load_models("my_package")
    """
    package = importlib.import_module(package_name)
    for _, module_name, is_pkg in pkgutil.iter_modules(package.__path__):
        if not is_pkg:
            importlib.import_module(f"{package_name}.{module_name}")
