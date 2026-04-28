# Registro Universal de Símbolos e Grandezas da Física
physics_registry = {
    "mecanica": {
        "cinematica": {
            "s": {"nome": "Posição/Espaço", "unidade": "m", "tipo": "escalar"},
            "v": {"nome": "Velocidade", "unidade": "m/s", "tipo": "vetorial"},
            "a": {"nome": "Aceleração", "unidade": "m/s²", "tipo": "vetorial"},
            "t": {"nome": "Tempo", "unidade": "s", "tipo": "escalar"},
            "v0": {"nome": "Velocidade Inicial", "unidade": "m/s", "tipo": "vetorial"}
        },
        "dinamica": {
            "m": {"nome": "Massa", "unidade": "kg", "tipo": "escalar"},
            "F": {"nome": "Força", "unidade": "N", "tipo": "vetorial"},
            "P": {"nome": "Peso", "unidade": "N", "tipo": "vetorial"},
            "g": {"nome": "Gravidade", "unidade": "m/s²", "tipo": "vetorial"},
            "W": {"nome": "Trabalho", "unidade": "J", "tipo": "escalar"},
            "Ec": {"nome": "Energia Cinética", "unidade": "J", "tipo": "escalar"},
            "Ep": {"nome": "Energia Potencial", "unidade": "J", "tipo": "escalar"}
        }
    },
    "termologia": {
        "T": {"nome": "Temperatura", "unidade": "K", "tipo": "escalar"},
        "Q": {"nome": "Calor Sensível", "unidade": "cal ou J", "tipo": "escalar"},
        "L": {"nome": "Calor Latente", "unidade": "cal/g", "tipo": "escalar"},
        "R": {"nome": "Constante dos Gases", "unidade": "J/(mol·K)", "tipo": "constante"}
    },
    "eletromagnetismo": {
        "U": {"nome": "Diferença de Potencial", "unidade": "V", "tipo": "escalar"},
        "i": {"nome": "Corrente Elétrica", "unidade": "A", "tipo": "escalar"},
        "R": {"nome": "Resistência", "unidade": "Ω", "tipo": "escalar"},
        "B": {"nome": "Campo Magnético", "unidade": "T", "tipo": "vetorial"},
        "phi": {"nome": "Fluxo Magnético", "unidade": "Wb", "tipo": "escalar"}
    },
    "ondas_optica": {
        "f": {"nome": "Frequência", "unidade": "Hz", "tipo": "escalar"},
        "lambda": {"nome": "Comprimento de Onda", "unidade": "m", "tipo": "escalar"},
        "n": {"nome": "Índice de Refração", "unidade": "adimensional", "tipo": "escalar"}
    },
    "fisica_moderna_constantes": {
        "c": {"nome": "Velocidade da Luz", "valor": 299792458, "unidade": "m/s"},
        "h": {"nome": "Constante de Planck", "valor": 6.626e-34, "unidade": "J·s"},
        "G": {"nome": "Constante Gravitacional", "valor": 6.674e-11, "unidade": "N·m²/kg²"}
    }
}