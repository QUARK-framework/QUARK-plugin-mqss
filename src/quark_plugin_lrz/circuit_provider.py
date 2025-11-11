from dataclasses import dataclass
from typing import override

from quark.core import Core, Data, Result
from quark.interface_types import InterfaceType, Circuit, Other, SampleDistribution

from qiskit import QuantumCircuit
from qiskit.qasm3 import dumps

@dataclass
class CircuitProvider(Core):
    """This module provides a simple entangling circuit to prepare a Bell state."""

    @override
    def preprocess(self, data: InterfaceType) -> Result:
        circuit = QuantumCircuit(2, 2)
        circuit.h(0)
        circuit.cx(0, 1)
        circuit.measure([0, 1], [0, 1])

        return Data(Circuit(dumps(circuit)))

    @override
    def postprocess(self, result: Other[dict] | SampleDistribution) -> Result:
        self.counts = []
        self.evs = []
        if isinstance(result, SampleDistribution):
            self.counts.append(result._samples)
        elif isinstance(result.data, dict):
            self.evs.append(result.data["expectation_values"])
        else:
            raise NotImplementedError
        return Data(Other(result))

    def get_metrics(self) -> dict:
        return {"counts": self.counts, "expectation_values": self.evs}
