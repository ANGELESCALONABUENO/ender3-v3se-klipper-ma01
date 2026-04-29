#!/usr/bin/env python3
import json
import os
import sys
import time
import urllib.request
import urllib.error


LOG_PATH = "/home/pi/printer_data/logs/spoolman_sync.log"


def _log(msg: str) -> None:
    ts = time.strftime("%Y-%m-%d %H:%M:%S")
    line = f"[{ts}] {msg}\n"
    try:
        with open(LOG_PATH, "a", encoding="utf-8") as f:
            f.write(line)
    except Exception:
        # Logging nunca debe romper el sync
        pass


def _http_json(url: str, method: str = "GET", body: dict | None = None, timeout_s: float = 10.0) -> dict:
    data = None
    headers = {"Accept": "application/json"}
    if body is not None:
        data = json.dumps(body).encode("utf-8")
        headers["Content-Type"] = "application/json"
    req = urllib.request.Request(url, data=data, headers=headers, method=method)
    with urllib.request.urlopen(req, timeout=timeout_s) as resp:
        raw = resp.read().decode("utf-8")
    return json.loads(raw) if raw else {}


def _post_gcode_with_retry(moonraker: str, script: str, attempts: int = 5) -> None:
    last_err: Exception | None = None
    for i in range(attempts):
        try:
            _http_json(
                f"{moonraker}/printer/gcode/script",
                method="POST",
                body={"script": script},
                timeout_s=10.0,
            )
            return
        except urllib.error.HTTPError as e:
            # 503 suele ocurrir cuando Klippy está reiniciando/no listo.
            if e.code == 503 and i < attempts - 1:
                last_err = e
                time.sleep(0.5 + (i * 0.5))
                continue
            raise
        except Exception as e:
            last_err = e
            if i < attempts - 1:
                time.sleep(0.5 + (i * 0.5))
                continue
            raise
    if last_err is not None:
        raise last_err


def main() -> int:
    spoolman_server = os.environ.get("SPOOLMAN_SERVER", "http://192.168.1.156:7912").rstrip("/")
    moonraker = os.environ.get("MOONRAKER", "http://127.0.0.1:7125").rstrip("/")

    _log(f"start moonraker={moonraker} spoolman={spoolman_server}")

    status = _http_json(f"{moonraker}/server/spoolman/status")
    spool_id = (status.get("result") or {}).get("spool_id")
    if spool_id in (None, "", "None"):
        # No spool activo, no es error
        _log("no active spool_id")
        print("spoolman_sync: no active spool_id")
        return 0

    spool = _http_json(f"{spoolman_server}/api/v1/spool/{spool_id}")
    filament = spool.get("filament") or {}

    # Datos cuantitativos del spool
    remaining_g = spool.get("remaining_weight")

    vendor_obj = filament.get("vendor")
    if isinstance(vendor_obj, dict):
        vendor = vendor_obj.get("name") or ""
    else:
        vendor = vendor_obj or ""
    filament_name = filament.get("name") or ""
    material = filament.get("material") or ""

    # Temperaturas recomendadas (si existen en Spoolman)
    nozzle_temp = filament.get("settings_extruder_temp")
    bed_temp = filament.get("settings_bed_temp")

    pa = None
    # En tu instancia real: filament.extra.pressure_advance (string)
    filament_extra = filament.get("extra") or {}
    for key in ("pressure_advance", "advance", "pa", "pressureAdvance", "pressure-advance"):
        val = filament_extra.get(key)
        if val not in (None, ""):
            pa = val
            break

    def sanitize_param(val: str) -> str:
        # Klipper params no soportan strings con espacios/comillas sin quoting,
        # y luego SET_GCODE_VARIABLE requiere un literal parseable.
        # Normalizamos a tokens seguros.
        return (
            str(val)
            .replace("\"", "")
            .replace("'", "")
            .replace(" ", "_")
            .strip()
        )

    script = "SYNC_SPOOLMAN_NOW"
    # Temperaturas/stock ayudan a monitoreo y a perfil Generic.
    try:
        if nozzle_temp not in (None, ""):
            script += f" NOZZLE={float(nozzle_temp)}"
    except Exception:
        pass
    try:
        if bed_temp not in (None, ""):
            script += f" BED={float(bed_temp)}"
    except Exception:
        pass
    try:
        if remaining_g not in (None, ""):
            script += f" REMAINING_G={float(remaining_g)}"
    except Exception:
        pass

    # Siempre enviar identidad/material para no heredar valores del spool anterior
    script += f" VENDOR={sanitize_param(vendor)}"
    script += f" FILAMENT_NAME={sanitize_param(filament_name)}"
    script += f" MATERIAL={sanitize_param(material)}"
    pa_f: float | None
    if pa is not None:
        try:
            pa_f = float(str(pa).strip())
        except Exception:
            pa_f = None
    else:
        pa_f = 0.1
    # Siempre enviar PA (si no viene en Spoolman, cae al default 0.1)
    if pa_f is not None:
        script += f" PRESSURE_ADVANCE={pa_f}"

    _post_gcode_with_retry(moonraker, script, attempts=6)

    _log(
        "ok "
        + f"spool_id={spool_id} vendor={vendor!r} name={filament_name!r} material={material!r} pa={pa!r} "
        + f"posted={script!r}"
    )
    print(f"spoolman_sync: ok spool_id={spool_id} vendor={vendor!r} name={filament_name!r} material={material!r} pa={pa!r}")
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except Exception as e:
        _log(f"error: {e!r}")
        print(f"spoolman_sync: error: {e}", file=sys.stderr)
        return_code = 1
        raise SystemExit(return_code)
