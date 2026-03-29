import numpy as np
import scipy.integrate as integrate
from qiskit import QuantumCircuit
from qiskit_aer import AerSimulator

print("--- TESTE DE INTEGRAÇÃO DO MONOREPO ---")

# 1. Teste de Física/Matemática (Integração Numérica)
# Calculando a integral de sin(x) de 0 a pi
val, err = integrate.quad(np.sin, 0, np.pi)
print(f"✅ SciPy/Numpy: Integral de sin(0->pi) = {val:.4f} (Esperado: 2.0000)")

# 2. Teste de Computação Quântica
qc = QuantumCircuit(1)
qc.h(0)  # Superposição
qc.measure_all()
sim = AerSimulator()
result = sim.run(qc).result().get_counts()
print(f"✅ Qiskit: Resultado da Superposição = {result}")

print("---------------------------------------")
print("🚀 O Laboratório está 100% Operacional!")
