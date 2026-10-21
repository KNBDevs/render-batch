FPS = 24
MOOD = 'happy'
ENV = 'patio'
META = {'title': '¿Flota o se hunde? 💧 ¿El corcho o el clavo? #shorts', 'description': 'Pimo y Luma prueban con el corcho y el clavo. Lo que tiene aire flota.\n\n#pimoruki #dibujosanimados #videosinfantiles #aprenderjugando #shorts', 'tags': ['pimoruki', 'dibujos animados', 'videos infantiles', 'aprender jugando', 'experimentos para niños', 'ciencia para niños', 'corcho', 'clavo', 'flota o se hunde', 'preescolar', 'pimo', 'shorts']}
AUTO = {'mech': 'flota', 'win': 'corcho', 'lose': 'clavo', 'order': ['corcho', 'clavo'], 'chars': ['pimo', 'luma'], 'heights': [1.8, 1.6], 'env': 'patio', 'look': 'atardecer', 'holiday': None, 'seed': 1792500205, 't0': 205, 'src': 'fallback'}
BASE = [('a1', 'pimo', '¡Vamos a probar algo!', 2.2), ('b1', 'luma', '¿Flotará el corcho o el clavo?', 3.4), ('a2', 'pimo', '¿Lo adivinas?', 1.9), ('b2', 'luma', '¡El corcho flota!', 3.2), ('a3', 'pimo', '¡El metal se hunde!', 3.4), ('b3', 'luma', '¡Probando se aprende!', 2.6)]
from auto.timing import layout
TOTAL, LINES, SFX = layout('exp_flota_corcho_clavo', BASE, AUTO)
