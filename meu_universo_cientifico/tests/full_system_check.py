import importlib
import sys
import time


def test_module(module_name, description):
    try:
        start = time.time()
        # Importação dinâmica para evitar que o script pare no primeiro erro
        mod = importlib.import_module(module_name)
        end = time.time()
        version = getattr(mod, "__version__", "N/A")
        print(f"✅ {description:.<30} OK (v{version}) [{end-start:.4f}s]")
        return True
    except ImportError:
        print(f"❌ {description:.<30} NÃO ENCONTRADO")
        return False
    except Exception as e:
        print(f"⚠️ {description:.<30} ERRO DE CARREGAMENTO: {e}")
        return False


print(f"--- DIAGNÓSTICO INTEGRAL DO MONOREPO ---")  # noqa: F541
print(f"Interpretador: {sys.executable}")
print(f"Versão Python: {sys.version.split()[0]}\n")

# Dicionário de Bibliotecas: {nome_do_modulo: "Descrição Amigável"}
bibliotecas = {
    "numpy": "Cálculo Numérico (Numpy)",
    "scipy": "Matemática Avançada (SciPy)",
    "matplotlib": "Gráficos (Matplotlib)",
    "pandas": "Análise de Dados (Pandas)",
    "qiskit": "Computação Quântica (Qiskit)",
    "qiskit_aer": "Simulador Quântico (Aer)",
    "rdkit": "Química Computacional (RDKit)",
    "mdtraj": "Biofísica (MDTraj)",
    "Bio": "Bioinformática (Biopython)",
    "astropy": "Astrofísica (Astropy)",
    "skyfield": "Astronomia (Skyfield)",
    "manim": "Animação Matemática (Manim)",
    "pygame": "Motor 2D (PyGame)",
    "ursina": "Motor 3D (Ursina)",
}

sucessos = 0
for mod, desc in bibliotecas.items():
    if test_module(mod, desc):
        sucessos += 1

print("-" * 50)
print(f"TOTAL: {sucessos}/{len(bibliotecas)} módulos operacionais.")

if sucessos == len(bibliotecas):
    print("\n🚀 LABORATÓRIO STATUS: PRONTO PARA EXPERIMENTAÇÃO.")
else:
    print("\n⚠️ ALERTA: Corrija as dependências ausentes antes de prosseguir.")
