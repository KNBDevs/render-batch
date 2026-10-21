FPS = 24
MOOD = 'calm'
ENV = 'lab'
META = {'title': '¿El tornillo o la pluma se pegará al imán? 🧲 #shorts', 'description': 'Descubre con Ruki y Moki por qué el imán solo atrae objetos hechos de hierro como el tornillo. Un experimento sencillo para aprender ciencia jugando.\n\n#pimoruki #dibujosanimados #videosinfantiles #aprenderjugando #shorts', 'tags': ['pimoruki', 'dibujos animados', 'videos infantiles', 'aprender jugando', 'experimentos para niños', 'ciencia para niños', 'tornillo', 'pluma', 'imanes', 'preescolar', 'ruki', 'shorts']}
AUTO = {'mech': 'iman', 'win': 'tornillo', 'lose': 'pluma', 'order': ['pluma', 'tornillo'], 'chars': ['ruki', 'moki'], 'heights': [1.7, 1.7], 'env': 'lab', 'look': 'foco', 'holiday': None, 'seed': 1792508508, 't0': 205, 'src': 'gemini'}
BASE = [('a1', 'ruki', '¡Mira: tornillo y pluma!', 2.2), ('b1', 'moki', '¿Cuál irá al imán: pluma o tornillo?', 3.4), ('a2', 'ruki', '¿Cuál crees? ¡A ver!', 1.9), ('b2', 'moki', '¡El tornillo se pega y la pluma no!', 3.2), ('a3', 'ruki', '¡El imán solo atrae cosas de hierro!', 3.4), ('b3', 'moki', '¡Qué magia tiene la ciencia!', 2.6)]
from auto.timing import layout
TOTAL, LINES, SFX = layout('exp_iman_tornillo_pluma', BASE, AUTO)
