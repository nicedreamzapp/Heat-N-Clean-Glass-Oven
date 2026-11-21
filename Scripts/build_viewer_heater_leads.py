"""Build viewer-heater-leads.html: the heater coil + lead connection drawn on the real
11-12 oven parts (viewer-full/*.glb, embedded so the page opens from file:// too)."""
import base64, json, pathlib

ROOT = pathlib.Path(__file__).resolve().parent.parent
PARTS = ["feet", "legscrews", "04", "spacer_bot", "bolts_bot", "03", "spacer_seat", "bolts_seat", "basedisk", "core", "01", "02"]

models = {p: "data:model/gltf-binary;base64," + base64.b64encode((ROOT / "viewer-full" / f"{p}.glb").read_bytes()).decode() for p in PARTS}
models["c1"] = "data:application/octet-stream;base64," + base64.b64encode((ROOT / "PRINT_SET_2026-11-12" / "STL" / "C1_Ceramic_Heater_Core.stl").read_bytes()).decode()
tpl = (ROOT / "Scripts" / "viewer_heater_leads_template.html").read_text()
(ROOT / "viewer-heater-leads.html").write_text(tpl.replace("__MODELS__", json.dumps(models)))
print("wrote viewer-heater-leads.html")
