"""Modelos e simulações quânticas (exemplo: QAOA, SAPQ)."""

from qiskit import QuantumCircuit

def executar_qaoa():
    qc = QuantumCircuit(2)
    qc.h(0)
    qc.cx(0, 1)
    return qc.draw()
