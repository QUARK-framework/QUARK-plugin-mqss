from dataclasses import dataclass
from time import sleep
from typing import override
import os

from quark.core import Core, Data, Result, Sleep
from quark.interface_types import InterfaceType, Other

from qiskit import QuantumCircuit
from mqss.qiskit_adapter import MQSSQiskitAdapter

lrz_token = os.getenv("LRZ_API_TOKEN")

@dataclass
class QlmMqss(Core):
    """
    This is an example module following the recommended structure for a quark module.

    A module must have a preprocess and postprocess method, as required by the Core abstract base class.
    A module's interface is defined by the type of data parameter those methods receive and return, dictating which other modules it can be connected to.
    Types defining interfaces should be chosen form QUARKs predefined set of types to ensure compatibility with other modules.
    """

    @override
    def preprocess(self, data: InterfaceType) -> Result:
        adapter = MQSSQiskitAdapter(token=lrz_token)
        backend = adapter.get_backend("QLM")

        # For testing
        circuit = QuantumCircuit(2, 2)
        circuit.h(0)
        circuit.cx(0, 1)
        circuit.measure([0, 1], [0, 1])
        # print(circuit)
        self.job = backend.run(circuit, shots=1000, qasm3=False)
        sleep(10) # Hardcoded sleep to wait until job ran through, will be handled by QUARK automatically in the future.
        return Data(Other(self.job))

    @override
    def postprocess(self, job: Other) -> Result:
        status = self.job.status()
        if str(status) == "JobStatus.DONE":
            result_dict = self.job.result().to_dict()
            self.counts = []
            for result in result_dict["results"]:
                self.counts.append(result["data"]["counts"])
        else:
            return Sleep(self.job) # This is how it will look like when Sleep feature is implemented.
        return Data(Other(result_dict))

    def get_metrics(self) -> dict:
        return {"counts": self.counts}
