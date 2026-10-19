OBJ = {
    "pelota": {"art": "la", "name": "pelota", "plural": False, "float": True, "roll": True, "magnet": False, "w": 2, "emoji": "⚽"},
    "corcho": {"art": "el", "name": "corcho", "float": True, "roll": False, "magnet": False, "w": 1, "emoji": "🍾"},
    "piedra": {"art": "la", "name": "piedra", "float": False, "roll": False, "magnet": False, "w": 5, "emoji": "🪨"},
    "manzana": {"art": "la", "name": "manzana", "float": True, "roll": True, "magnet": False, "w": 3, "emoji": "🍎"},
    "naranja": {"art": "la", "name": "naranja", "float": True, "roll": True, "magnet": False, "w": 3, "emoji": "🍊"},
    "madera": {"art": "el", "name": "bloque de madera", "float": True, "roll": False, "magnet": False, "w": 3, "emoji": "🪵"},
    "hoja": {"art": "la", "name": "hoja", "float": True, "roll": False, "magnet": False, "w": 0, "emoji": "🍃"},
    "pluma": {"art": "la", "name": "pluma", "float": True, "roll": False, "magnet": False, "w": 0, "emoji": "🪶"},
    "canica": {"art": "la", "name": "canica", "float": False, "roll": True, "magnet": False, "w": 2, "emoji": "🔮"},
    "clavo": {"art": "el", "name": "clavo", "float": False, "roll": False, "magnet": True, "w": 1, "emoji": "🔩"},
    "clip": {"art": "el", "name": "clip", "float": False, "roll": False, "magnet": True, "w": 0, "emoji": "📎"},
    "tornillo": {"art": "el", "name": "tornillo", "float": False, "roll": False, "magnet": True, "w": 1, "emoji": "🔩"},
    "libro": {"art": "el", "name": "libro", "float": False, "roll": False, "magnet": False, "w": 5, "emoji": "📘"},
    "rueda": {"art": "la", "name": "rueda", "float": True, "roll": True, "magnet": False, "w": 2, "emoji": "🛞"},
    "caja": {"art": "la", "name": "caja", "float": True, "roll": False, "magnet": False, "w": 2, "emoji": "📦"},
}

MECH = {
    "flota": {"yes": ["pelota", "corcho", "manzana", "naranja", "madera", "hoja"], "no": ["piedra", "canica", "clavo", "tornillo"],
              "verb_yes": "flota", "verb_no": "se hunde", "q": "¿Cuál flotará?", "emoji": "💧",
              "rule": "Lo que tiene aire dentro o es de madera o corcho flota; el metal, el cristal y las piedras se hunden.", "env": ["patio", "lab", "casa"]},
    "rueda": {"yes": ["pelota", "canica", "naranja", "rueda", "manzana"], "no": ["madera", "libro", "caja"],
              "verb_yes": "rueda", "verb_no": "se queda quieto", "q": "¿Cuál rodará por la rampa?", "emoji": "🛝",
              "rule": "Lo redondo rueda; lo que tiene lados planos se queda quieto.", "env": ["patio", "plaza", "aula"]},
    "iman": {"yes": ["clavo", "clip", "tornillo"], "no": ["hoja", "pelota", "madera", "corcho", "manzana", "pluma"],
             "verb_yes": "se pega al imán", "verb_no": "no se mueve", "q": "¿Cuál se pegará al imán?", "emoji": "🧲",
             "rule": "El imán atrae cosas de hierro, como clavos y clips; la madera, el plástico y las hojas, no.", "env": ["lab", "aula", "casa"]},
    "pesa": {"yes": ["piedra", "libro", "naranja", "manzana"], "no": ["pluma", "hoja"],
             "verb_yes": "pesa más", "verb_no": "pesa menos", "q": "¿Cuál pesará más?", "emoji": "⚖️",
             "rule": "La balanza baja del lado de lo que pesa más.", "env": ["casa", "aula", "patio"]},
}

PAIRS = [("pimo", "luma"), ("ruki", "moki"), ("tuki", "bolita"), ("bopi", "luma"), ("pimo", "bolita"), ("moki", "pimo"), ("tuki", "ruki")]
HEIGHT = {"pimo": 1.8, "luma": 1.6, "ruki": 1.7, "moki": 1.7, "tuki": 1.6, "bolita": 1.5, "bopi": 1.6, "gruno": 1.85}
NAME = {"pimo": "Pimo", "luma": "Luma", "ruki": "Ruki", "moki": "Moki", "tuki": "Tuki", "bolita": "Bolita", "bopi": "Bopi", "gruno": "Gruño"}
LOOKS = ["dia", "atardecer", "foco", "fresco"]

HOLIDAYS = [
    {"id": "navidad", "from": (12, 1), "to": (12, 26), "label": "Navidad", "emoji": "🎄"},
    {"id": "reyes", "from": (12, 27), "to": (1, 6), "label": "Reyes", "emoji": "👑"},
    {"id": "sanvalentin", "from": (2, 7), "to": (2, 14), "label": "San Valentín", "emoji": "💖"},
    {"id": "carnaval", "from": None, "to": None, "label": "Carnaval", "emoji": "🎭", "easter_offset": (-52, -47)},
    {"id": "pascua", "from": None, "to": None, "label": "Pascua", "emoji": "🐣", "easter_offset": (-7, 1)},
    {"id": "verano", "from": (6, 21), "to": (6, 30), "label": "Verano", "emoji": "☀️"},
    {"id": "otono", "from": (9, 22), "to": (10, 20), "label": "Otoño", "emoji": "🍂"},
    {"id": "halloween", "from": (10, 21), "to": (10, 31), "label": "Halloween", "emoji": "🎃"},
    {"id": "invierno", "from": (12, 21), "to": (12, 31), "label": "Invierno", "emoji": "❄️"},
]


def label(o, cap=False):
    d = OBJ[o]
    s = f"{d['art']} {d['name']}"
    return s[0].upper() + s[1:] if cap else s
