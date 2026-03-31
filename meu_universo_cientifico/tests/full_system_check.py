import importlib
import sys
import time
from pathlib import Path

# --- CONFIGURAÇÃO DE ACESSO AO MÓDULO KEYS ---
# Define a raiz subindo um nível (de /tests para /)
raiz = Path(__file__).resolve().parent.parent
sys.path.append(str(raiz))

try:
    from keys.keys import MINHA_CHAVE, validar_conexao

    if validar_conexao():
        print(f"✅ Autenticado via módulo keys. Chave: {MINHA_CHAVE[:4]}...") # type: ignore
    else:
        print("⚠️ Módulo keys encontrado, mas chave não carregada (verifique o .env).")
except Exception as e:
    print(f"❌ Erro ao importar módulo de chaves: {e}")


# --- FUNÇÃO DE TESTE DE MÓDULOS ---
def test_module(module_name, description):
    try:
        start = time.time()
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


print("\n--- DIAGNÓSTICO INTEGRAL DO MONOREPO ---")
print(f"Interpretador: {sys.executable}")
print(f"Versão Python: {sys.version.split()[0]}\n")

# Dicionário de Bibliotecas
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
