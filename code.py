import time, json
import usb_hid
from adafruit_hid.keyboard import Keyboard
from adafruit_hid.keycode import Keycode
from adafruit_hid.mouse import Mouse

kbd = Keyboard(usb_hid.devices)
mouse = Mouse(usb_hid.devices)

def log(msg):
    print(f"[{time.monotonic():.2f}] {msg}")

def normalizar_si_no(valor, por_defecto=False):
    if valor is None:
        return por_defecto
    if isinstance(valor, bool):
        return valor
    if isinstance(valor, (int, float)):
        return valor != 0
    s = str(valor).strip().lower()
    s = s.replace("í", "i")  # In case "sí" is used.
    return s in ("si", "s", "true", "1", "on", "yes")

def alt_esc():
    kbd.press(Keycode.LEFT_ALT, Keycode.ESCAPE)
    time.sleep(0.05)
    kbd.release_all()

def ir_a_home(veces):
    for _ in range(max(0, int(veces))):
        alt_esc()
        time.sleep(0.25)

def reiniciar_puntero():
    mouse.move(-3000, -3000)
    time.sleep(0.2)

def click_rel(dx, dy, delay_ms=150):
    mouse.move(int(dx), int(dy))
    time.sleep(delay_ms/1000)
    mouse.click(Mouse.LEFT_BUTTON)
    time.sleep(0.2)

def scroll(direccion, ticks):
    # In many systems: negative wheel = up, positive wheel = down.
    ticks = abs(int(ticks))
    direccion = (direccion or "").strip().lower()
    paso = 20
    pausa = 0.03
    if direccion in ("arriba", "up"):
        paso = -paso
    else:
        paso = abs(paso)

    restante = ticks
    while restante > 0:
        movimiento = min(abs(paso), restante)
        if paso < 0:
            movimiento = -movimiento
        mouse.move(wheel=movimiento)
        restante -= abs(movimiento)
        time.sleep(pausa)

    time.sleep(0.1)

with open("macro.json", "r") as f:
    cfg = json.load(f)

conf = cfg.get("configuracion", {})
reiniciar_inicio = normalizar_si_no(conf.get("reiniciar_puntero_al_inicio"), True)
reiniciar_antes_click = normalizar_si_no(conf.get("reiniciar_puntero_antes_de_cada_click"), True)
delay_entre_pasos_ms = int(conf.get("delay_entre_pasos_ms", 150))

if reiniciar_inicio:
    reiniciar_puntero()

secciones = cfg.get("secciones", [])
log(f"Sections: {len(secciones)}")

for sec in secciones:
    desc = sec.get("descripcion", "(sin descripcion)")
    activo = normalizar_si_no(sec.get("activo"), True)

    if not activo:
        log(f"Skipping (inactive): {desc}")
        continue

    log(f"Running: {desc}")
    pasos = sec.get("pasos", [])
    delay_sec_ms = int(sec.get("delay_entre_pasos_ms", delay_entre_pasos_ms))

    for paso in pasos:
        tipo = (paso.get("tipo") or "").strip().lower()

        if tipo == "esperar":
            time.sleep(float(paso.get("segundos", 0)))
        elif tipo == "ir_a_home":
            ir_a_home(paso.get("veces", 1))
        elif tipo == "click":
            if reiniciar_antes_click:
                reiniciar_puntero()
            click_rel(paso.get("dx", 0), paso.get("dy", 0), delay_sec_ms)
        elif tipo == "clicks":
            lista = paso.get("lista", [])
            for c in lista:
                if reiniciar_antes_click:
                    reiniciar_puntero()
                click_rel(c.get("dx", 0), c.get("dy", 0), delay_sec_ms)
        elif tipo == "scroll":
            scroll(paso.get("direccion", "arriba"), paso.get("ticks", 40))
        else:
            log(f"Unknown step: {tipo} (ignored)")

        time.sleep(delay_sec_ms / 1000)

log("Macro finished.")
while True:
    time.sleep(1)
