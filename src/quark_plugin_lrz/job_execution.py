from dataclasses import dataclass
from typing import override

from quark.core import Core, Data, Result
from quark.interface_types import Other, Circuit, SampleDistribution

import qiskit.qasm3
from mqss.qiskit_adapter import MQSSQiskitAdapter


@dataclass
class JobExecution(Core):
    """
    This module executes a quantum circuit on the MQSS backend using the Qiskit adapter.
    """
    shots: int = 10
    token: str = "" # Add your valid token here
    backend_name: str = None # You can specify a backend name, e.g., "QLM"

    @override
    def preprocess(self, data: Circuit) -> Result:
        circuit = qiskit.qasm3.loads(data.as_qasm_string())
        adapter = MQSSQiskitAdapter(token=self.token)
        backend = adapter.get_backend(self.backend_name)
        self.job = backend.run(circuit, shots=self.shots, qasm3=False)
        return Data(Other(self.job))

    @override
    def postprocess(self, job: Other) -> Result:
        result_as_list = []
        raw_result_dict = self.job.result().to_dict()
        result_as_dict = raw_result_dict["results"][0]["data"]["counts"]
        for qubit_string in result_as_dict:
            result_as_list.append((qubit_string, result_as_dict[qubit_string]))
        return Data(SampleDistribution.from_list(result_as_list, self.shots))
