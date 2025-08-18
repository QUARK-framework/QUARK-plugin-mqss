from dataclasses import dataclass
from time import sleep
from typing import override
import os

from quark.core import Core, Data, Result
from quark.interface_types import InterfaceType, Other

from qiskit import QuantumCircuit
from mqss.qiskit_adapter import MQSSQiskitAdapter

from qat.lang.AQASM import Program, H, CNOT
from qat.interop.qiskit import qlm_to_qiskit


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
        # circuit = QuantumCircuit(2, 2)
        # circuit.h(0)
        # circuit.cx(0, 1)
        # circuit.measure([0, 1], [0, 1])
        # job = backend.run(circuit, shots=1000)
        ### From https://myqlm.github.io/05_demos.html
        # Create a Program
        qprog = Program()
        # Number of qbits
        nbqbits = 2
        # Allocate some qbits
        qbits = qprog.qalloc(nbqbits)

        # Apply some quantum Gates
        qprog.apply(H, qbits[0])
        qprog.apply(CNOT, qbits[0], qbits[1])

        # Export this program into a quantum circuit
        circuit = qprog.to_circ()
        qiskit_circuit = qlm_to_qiskit(circuit)
        # And display it!
        # circuit.display()
        job = backend.run(qiskit_circuit, shots=1000)

        print(job.result().get_results())
        return Data(Other(job))

    @override
    def postprocess(self, job: Other) -> Result:
        status = job.status()
        print("Job status:", status)
        if status == "COMPLETED":
            result = job.result()
            counts = result.get_counts()
            result_dict = job.result().to_dict()
            print("Counts:", counts)
        else:
            sleep(10)
            self.postprocess(Data(Other(job)))
        return result_dict
