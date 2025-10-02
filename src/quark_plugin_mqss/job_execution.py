from dataclasses import dataclass
from typing import override
import os

from quark.core import Core, Data, Result
from quark.interface_types import Other, Circuit

import qiskit.qasm3
from qiskit import QuantumCircuit
from mqss.qiskit_adapter import MQSSQiskitAdapter

lrz_token = os.getenv("LRZ_API_TOKEN")

@dataclass
class JobExecution(Core):
    """
    This module executes a quantum circuit on the MQSS backend using the Qiskit adapter.
    """

    @override
    def preprocess(self, data: Circuit) -> Result:
        circuit = qiskit.qasm3.loads(data.as_qasm_string())
        adapter = MQSSQiskitAdapter(token=lrz_token)
        backend = adapter.get_backend("QLM")
        self.job = backend.run(circuit, shots=1000, qasm3=False)
        return Data(Other(self.job))

    @override
    def postprocess(self, job: Other) -> Result:
        result_dict = self.job.result().to_dict()
        return Data(Other(result_dict))
