from quark.plugin_manager import factory

<<<<<<<< HEAD:src/quark_plugin_mqss/__init__.py
from quark_plugin_mqss.circuit_provider import CircuitProvider
from quark_plugin_mqss.job_execution import JobExecution
========
from PLUGIN_NAME_FORMATTED.example_module import ExampleModule
>>>>>>>> parent of 04c6ac3 (Apply automatic changes):src/PLUGIN_NAME_FORMATTED/__init__.py

def register() -> None:
    """
    Register all modules exposed to quark by this plugin.
    For each module, add a line of the form:
        factory.register("module_name", Module)

    The "module_name" will later be used to refer to the module in the configuration file.
    """
    factory.register("circuit_provider", CircuitProvider)
    factory.register("job_execution", JobExecution)
