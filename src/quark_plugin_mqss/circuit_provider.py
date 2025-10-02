from dataclasses import dataclass
from typing import override

from quark.core import Core, Data, Result
from quark.interface_types import InterfaceType, Circuit, Other

from qiskit import QuantumCircuit
from qiskit.qasm3 import dumps

@dataclass
class CircuitProvider(Core):
    """This module provides a simple entangling circuit for testing purposes."""

    @override
    def preprocess(self, data: InterfaceType) -> Result:
        # For testing
        circuit = QuantumCircuit(2, 2)
        circuit.h(0)
        circuit.cx(0, 1)
        circuit.measure([0, 1], [0, 1])

        return Data(Circuit(dumps(circuit)))

    @override
    def postprocess(self, result: Other[dict]) -> Result:
        self.counts = []
        for res in result.data["results"]:
            self.counts.append(res["data"]["counts"])
        return Data(Other(result))

    def get_metrics(self) -> dict:
        return {"counts": self.counts}
