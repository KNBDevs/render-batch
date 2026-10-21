import json, os, sys, random, re, subprocess, time, urllib.request, urllib.error, unicodedata
from datetime import datetime, timezone, timedelta, date
HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path[:0] = [ROOT, HERE]
from catalog import OBJ, MECH, PAIRS, HEIGHT, NAME, LOOKS, HOLIDAYS, label

QUEUE = os.path.join(ROOT, "catalog", "queue.json")
USED = os.path.join(ROOT, "catalog", "auto_used.json")
SCHED = os.path.join(ROOT, "state", "schedule.json")
PUB = os.path.join(ROOT, "state", "published.json")
STATS = os.path.join(ROOT, "state", "stats.json")
KEY = os.environ.get("GEMINI_API_KEY", "")
MODEL = os.environ.get("TEXT_MODEL", "")
TOTAL = 720
LOG = []
CANDS = []
LOGF = os.path.join(ROOT, "catalog", "auto_log.json")
T0 = 205
FRAMES = [10, 66, 152, 440, 522, 612]
MAXS = [2.2, 3.4, 1.9, 3.2, 3.4, 2.6]
LIMS = [int(m * 11) for m in MAXS]
TRAIT = {"pimo": "curioso y preguntón", "luma": "alegre y risueña", "ruki": "tranquilo y sereno", "moki": "soñador y dulce",
         "tuki": "juguetón y enérgico", "bolita": "valiente e impulsiva", "bopi": "robot ordenado que dice bip bop", "gruno": "inventor presumido"}
SHORT_RULE = {"flota": "Lo que tiene aire flota.", "rueda": "Lo redondo rueda.",
              "iman": "El imán atrae el hierro.", "pesa": "Baja el lado que pesa más."}
QSHORT = {"flota": "¿Flota o se hunde?", "rueda": "¿Rueda o no rueda?", "iman": "¿Se pega al imán?", "pesa": "¿Cuál pesa más?"}


def norm(t):
    return "".join(c for c in unicodedata.normalize("NFD", t.lower()) if unicodedata.category(c) != "Mn")


def easter(y):
    a, b, c = y % 19, y // 100, y % 100
    d, e = b // 4, b % 4
    f = (b + 8) // 25
    g = (b - f + 1) // 3
    h = (19 * a + b - d - g + 15) % 30
    i, k = c // 4, c % 4
    l = (32 + 2 * e + 2 * i - h - k) % 7
    m = (a + 11 * h + 22 * l) // 451
    mo = (h + l - 7 * m + 114) // 31
    da = (h + l - 7 * m + 114) % 31 + 1
    return date(y, mo, da)


def holiday_for(d):
    for h in HOLIDAYS:
        if h.get("easter_offset"):
            e = easter(d.year)
            a, b = (e + timedelta(days=x) for x in h["easter_offset"])
        else:
            a = date(d.year, *h["from"])
            b = date(d.year, *h["to"])
            if b < a:
                if d >= a:
                    b = date(d.year + 1, *h["to"])
                else:
                    a = date(d.year - 1, *h["from"])
        if a <= d <= b and h["id"] not in ("halloween",):
            return h
    return None


def load(p, default):
    return json.load(open(p)) if os.path.exists(p) else default


def buffer_state():
    now = datetime.now(timezone.utc)
    sched = load(SCHED, {})
    pub = set(load(PUB, []))
    q = load(QUEUE, [])
    fut = sorted(datetime.fromisoformat(v.replace("Z", "+00:00")) for v in sched.values())
    fut = [t for t in fut if t > now]
    pending = [e for e in q if e.get("status") == "approved" and e["id"] not in pub and not e.get("publish_local")]
    slots = len(fut) + len(pending)
    last = max([t.date() for t in fut] + [now.date()])
    air = last + timedelta(days=1 + len(pending) // 2)
    return slots / 2.0, air


def weights():
    st = load(STATS, {})
    perf = {}
    for r in st.values():
        e = r.get("episode") or ""
        if not e.startswith("exp_") or not r.get("hist"):
            continue
        m = e.split("_")[1]
        perf.setdefault(m, []).append(list(r["hist"].values())[-1][0] or 0)
    return {m: 1.0 + (sum(v) / len(v)) / 2000.0 if v else 1.5 for m, v in ((m, perf.get(m, [])) for m in MECH)}


def pick(used, rnd, avoid=()):
    w = weights()
    mechs = list(MECH)
    rnd.shuffle(mechs)
    mechs.sort(key=lambda m: -w[m] * rnd.uniform(0.6, 1.4))
    mechs = [m for m in mechs if m not in avoid] + [m for m in mechs if m in avoid]
    for strict in (True, False):
        for m in mechs:
            M = MECH[m]
            combos = [(y, n) for y in M["yes"] for n in M["no"]]
            rnd.shuffle(combos)
            for y, n in combos:
                key = f"{m}|{y}|{n}"
                pair = rnd.choice([p for p in PAIRS if not set(p) & set(avoid)] or PAIRS)
                k2 = f"{key}|{'-'.join(pair)}"
                if strict and key in used:
                    continue
                if not strict and k2 in used:
                    continue
                return m, y, n, pair
    return None


def model():
    global MODEL
    if MODEL:
        return MODEL
    r = urllib.request.Request("https://generativelanguage.googleapis.com/v1beta/models?pageSize=200", headers={"x-goog-api-key": KEY})
    ms = json.load(urllib.request.urlopen(r, timeout=60)).get("models", [])
    bad = ("tts", "image", "live", "embed", "audio", "vision", "exp", "preview", "thinking", "lite", "learnlm", "gemma", "aqa", "robotics", "computer")
    ok = [m["name"].split("/")[-1] for m in ms if "generateContent" in m.get("supportedGenerationMethods", [])]
    pref = [n for n in ok if "flash" in n and not any(b in n for b in bad)] or [n for n in ok if "flash" in n and "tts" not in n and "image" not in n] or ok
    pref.sort(key=lambda n: [int(x) if x.isdigit() else 0 for x in re.findall(r"\d+", n)], reverse=True)
    CANDS[:] = pref[:4]
    MODEL = pref[0]
    LOG.append({"models": CANDS})
    return MODEL


def gemini(prompt):
    global MODEL
    model()
    last = None
    for name in [MODEL] + [c for c in CANDS if c != MODEL]:
        for wait in (0, 20, 45):
            time.sleep(wait)
            try:
                return gemini_one(prompt, name)
            except urllib.error.HTTPError as e:
                last = e
                if e.code not in (429, 500, 503):
                    raise
    raise last


def gemini_one(prompt, name):
    body = {"contents": [{"parts": [{"text": prompt}]}],
            "generationConfig": {"responseMimeType": "application/json", "temperature": 1.0}}
    r = urllib.request.Request(f"https://generativelanguage.googleapis.com/v1beta/models/{name}:generateContent",
                               data=json.dumps(body).encode(), headers={"x-goog-api-key": KEY, "Content-Type": "application/json"})
    d = json.load(urllib.request.urlopen(r, timeout=120))
    return json.loads(d["candidates"][0]["content"]["parts"][0]["text"])


def facts(m, y, n, pair, hol):
    M = MECH[m]
    a, b = pair
    return {
        "experimento": M["q"], "objeto_que_si": label(y), "resultado_si": M["verb_yes"],
        "objeto_que_no": label(n), "resultado_no": M["verb_no"], "explicacion": M["rule"],
        "personaje_A": f"{NAME[a]} ({TRAIT[a]})", "personaje_B": f"{NAME[b]} ({TRAIT[b]})",
        "fiesta": hol["label"] if hol else None,
    }


PROMPT = """Escribe el guion de un Short de dibujos animados 3D para niños de 3 a 6 años, en castellano de España (tuteo, nada latinoamericano), cálido, divertido y claro.
Formato: dos personajes hacen un experimento sencillo y el niño intenta adivinar el resultado.
Datos (son correctos; no inventes otros resultados): {facts}
Devuelve SOLO JSON con esta forma:
{{"lineas": [6 frases], "titulo": "...", "descripcion": "..."}}
Reglas de las 6 frases (orden fijo; A dice 1, 3 y 5; B dice 2, 4 y 6):
1 (A, máx {l0} caracteres): gancho sorprendente que presenta los dos objetos.
2 (B, máx {l1} caracteres): la pregunta de predicción, nombrando los dos objetos.
3 (A, máx {l2} caracteres): invita al niño a adivinar (p. ej. «¿Tú qué crees?») y anuncia la prueba.
4 (B, máx {l3} caracteres): resultado, nombrando qué objeto {ys} y cuál {ns}.
5 (A, máx {l4} caracteres): explicación muy simple y verdadera basada en la explicación dada.
6 (B, máx {l5} caracteres): cierre alegre y breve. Si hay fiesta, menciónala con cariño aquí.
Frases cortas y naturales para decir en voz alta, con exclamaciones o preguntas. Sin pedir suscripciones, likes ni comentarios. Sin sustos.
titulo: máx 80 caracteres, con una pregunta de predicción binaria que nombre los dos objetos y un emoji; sin hashtags.
descripcion: 1-2 frases sencillas sobre lo que se aprende."""


def valid(js, m, y, n):
    L = js.get("lineas")
    if not isinstance(L, list) or len(L) != 6:
        return "lineas"
    for i, (t, lim) in enumerate(zip(L, LIMS)):
        if not isinstance(t, str):
            return f"tipo {i}"
        t = t.strip()
        if not (4 <= len(t) <= lim):
            return f"long {i} {len(t)}>{lim}"
        if re.sub(r"[\s\u200d\ufe0f\u2600-\u27bf\U0001F000-\U0001FAFF]+$", "", t)[-1:] not in "!?.…»":
            return f"fin {i}"
    blob = norm(" ".join(L) + js.get("titulo", ""))
    for w in ("suscri", "like", "comenta", "campanita", "susto", "miedo"):
        if w in blob:
            return f"veto {w}"
    ny, nn = norm(OBJ[y]["name"]).split()[-1], norm(OBJ[n]["name"]).split()[-1]
    if ny not in norm(L[1]) or nn not in norm(L[1]):
        return "pregunta sin objetos"
    if ny not in norm(L[3]):
        return "resultado sin objeto"
    t = js.get("titulo", "")
    if not (10 <= len(t) <= 85 and "?" in t and "#" not in t):
        return f"titulo {t}"
    return None


def fallback(m, y, n, pair, hol, rnd):
    M = MECH[m]
    Y, N = label(y), label(n)
    l1 = rnd.choice(["¡Hoy toca experimento!", "¡Mira qué tengo!", "¡Vamos a probar algo!"])
    l2 = {"flota": f"¿Flotará {Y} o {N}?", "rueda": f"¿Rodará {Y} o {N}?", "iman": f"¿Se pegará {Y} o {N}?", "pesa": f"¿Pesará más {Y} o {N}?"}[m]
    l3 = rnd.choice(["¿Tú qué crees?", "¿Lo adivinas?", "¡Piensa! ¡A ver!"])
    l4 = f"¡{Y[0].upper() + Y[1:]} {M['verb_yes']}!"
    l5 = SHORT_RULE[m]
    if m == "flota":
        l5 = {"clavo": "¡El metal se hunde!", "tornillo": "¡El metal se hunde!", "piedra": "¡Las piedras se hunden!", "canica": "¡El cristal se hunde!"}[n]
    l6 = f"¡Feliz {hol['label']}!" if hol else rnd.choice(["¡Probando se aprende!", "¡Qué experimento!", "¡Otra vez, otra vez!"])
    t = f"{QSHORT[m]} {M['emoji']} ¿{Y[0].upper() + Y[1:]} o {N}?"
    d = f"{NAME[pair[0]]} y {NAME[pair[1]]} prueban con {Y} y {N}. {SHORT_RULE[m]}"
    return {"lineas": [l1, l2, l3, l4, l5, l6], "titulo": t, "descripcion": d}


def script(m, y, n, pair, hol, rnd):
    if KEY:
        f = json.dumps(facts(m, y, n, pair, hol), ensure_ascii=False)
        M = MECH[m]
        p = PROMPT.format(facts=f, l0=LIMS[0], l1=LIMS[1], l2=LIMS[2], l3=LIMS[3], l4=LIMS[4], l5=LIMS[5], ys=M["verb_yes"], ns=M["verb_no"])
        for _ in range(3):
            try:
                js = gemini(p)
                if isinstance(js, dict) and "lineas" in js:
                    js["lineas"] = [x.strip() for x in js["lineas"]]
                why = valid(js, m, y, n)
                LOG.append({"t": datetime.now(timezone.utc).isoformat()[:19], "ok": not why, "why": why})
                if not why:
                    js["source"] = "gemini"
                    return js
                print("invalid", why, json.dumps(js, ensure_ascii=False)[:300], flush=True)
            except Exception as e:
                LOG.append({"t": datetime.now(timezone.utc).isoformat()[:19], "ok": False, "why": str(e)[:200]})
                print("gemini err", e, flush=True)
    js = fallback(m, y, n, pair, hol, rnd)
    js["source"] = "fallback"
    return js


def sfx(m, win, order):
    out = [(6, "pop", 0.25)]
    for k, kind in enumerate(order):
        f = T0 + k * (80 if m == "pesa" else 100)
        w = kind == win
        if m == "flota":
            out += [(f + 16, "boing_up", 0.15), (f + 31, "splat", 0.22), (f + 44, "bip", 0.12) if w else (f + 64, "clonk", 0.25)]
        elif m == "rueda":
            out.append((f - 30, "boing_up", 0.12))
            out += [(f + 12, "whistle_down", 0.12), (f + 58, "tock", 0.2)] if w else [(f + 12, "tock", 0.2), (f + 22, "bip", 0.12)]
        elif m == "iman":
            out += [(f + 20, "bip", 0.15), (f + 28, "clonk", 0.3) if w else (f + 30, "whistle_down", 0.08)]
        else:
            out += [(f, "boing_up", 0.12), (f + 12, "clonk", 0.22)]
    if m == "pesa":
        out.append((T0 + 102, "whistle_down", 0.1))
    out += [(FRAMES[3], "sparkle", 0.22), (FRAMES[5] + 6, "popper", 0.25)]
    return sorted(out)


def write(eid, m, y, n, pair, hol, js, rnd, seed):
    M = MECH[m]
    a, b = pair
    order = [y, n] if rnd.random() < 0.5 else [n, y]
    env = rnd.choice(M["env"])
    look = rnd.choice(LOOKS)
    who = [a, b, a, b, a, b]
    keys = ["a1", "b1", "a2", "b2", "a3", "b3"]
    base = [(k, c, t, mx) for k, c, t, mx in zip(keys, who, js["lineas"], MAXS)]
    emo = (hol["emoji"] + " ") if hol else ""
    title = f"{js['titulo'].strip()} {emo}#shorts".replace("  ", " ")[:100]
    desc = (js["descripcion"].strip() + "\n\n#pimoruki #dibujosanimados #videosinfantiles #aprenderjugando #shorts")
    tags = ["pimoruki", "dibujos animados", "videos infantiles", "aprender jugando", "experimentos para niños", "ciencia para niños",
            OBJ[y]["name"], OBJ[n]["name"], {"flota": "flota o se hunde", "rueda": "rodar", "iman": "imanes", "pesa": "balanza"}[m],
            "preescolar", NAME[a].lower(), "shorts"]
    auto = {"mech": m, "win": y, "lose": n, "order": order, "chars": [a, b], "heights": [HEIGHT[a], HEIGHT[b]],
            "env": env, "look": look, "holiday": hol["id"] if hol else None, "seed": seed, "t0": T0, "src": js.get("source")}
    src = ["FPS = 24", "MOOD = " + repr(rnd.choice(["happy", "silly", "calm"])), f"ENV = {env!r}",
           "META = " + repr({"title": title, "description": desc, "tags": tags}), "AUTO = " + repr(auto),
           "BASE = " + repr(base), "from auto.timing import layout",
           f"TOTAL, LINES, SFX = layout({eid!r}, BASE, AUTO)"]
    open(os.path.join(ROOT, "episodes", f"{eid}_plan.py"), "w").write("\n".join(src) + "\n")
    open(os.path.join(ROOT, "episodes", f"{eid}_scene.py"), "w").write(f"from auto.scene import build\nbuild({eid!r})\n")
    subprocess.run([sys.executable, os.path.join(ROOT, "props", "record.py"), eid, env], check=False, stdout=subprocess.DEVNULL)
    return title


def make(n_max, force=False):
    days, air = buffer_state()
    print("buffer days", days, "air", air, flush=True)
    need = n_max if force else (n_max if days < 4 else 0)
    if not need:
        return []
    used = load(USED, {})
    q = load(QUEUE, [])
    made = []
    made_info = []
    for i in range(need):
        seed = int(datetime.now(timezone.utc).timestamp()) + i * 7919
        rnd = random.Random(seed)
        ch = pick(used, rnd, [x for e in made_info for x in e])
        if not ch:
            break
        m, y, n, pair = ch
        hol = holiday_for(air + timedelta(days=i // 2))
        js = script(m, y, n, pair, hol, rnd)
        eid = f"exp_{m}_{y}_{n}"
        k = 2
        while os.path.exists(os.path.join(ROOT, "episodes", f"{eid}_plan.py")):
            eid = f"exp_{m}_{y}_{n}_{k}"
            k += 1
        title = write(eid, m, y, n, pair, hol, js, rnd, seed)
        used[f"{m}|{y}|{n}"] = eid
        used[f"{m}|{y}|{n}|{'-'.join(pair)}"] = eid
        q.append({"id": eid, "template": "episode", "title": title.split(" #")[0], "cast": list(pair), "status": "approved", "auto": True})
        made.append(eid)
        made_info.append((m, pair[0], pair[1]))
        print("made", eid, js.get("source"), "|", title, flush=True)
    json.dump(used, open(USED, "w"), ensure_ascii=False, indent=1)
    old = load(LOGF, [])
    json.dump((old + LOG)[-30:], open(LOGF, "w"), ensure_ascii=False, indent=1)
    json.dump(q, open(QUEUE, "w"), ensure_ascii=False, indent=2)
    return made


if __name__ == "__main__":
    n = int(sys.argv[1]) if len(sys.argv) > 1 else 2
    print(" ".join(make(n, force="--force" in sys.argv)))
