try:
    from qiskit_aer import AerSimulator

    sim = AerSimulator()
    print("✅ Qiskit Aer carregado e inicializado com sucesso!")
except ImportError as e:
    print(f"❌ Erro de importação: {e}")
except Exception as e:
    print(f"⚠️ Erro inesperado: {e}")
