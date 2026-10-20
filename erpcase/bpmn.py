"""BPMN 2.0 XML (with diagram interchange) and an SVG rendering from one process definition.

The definitions live in data/processes.json. The .bpmn files open in Camunda Modeler or
bpmn.io; the SVG is what the site and the Markdown show. Both use the same coordinates.
"""
from __future__ import annotations

from xml.sax.saxutils import escape

COL_W, LANE_H, LEFT, TOP = 150, 140, 70, 20
ROW_DY = 46
SIZE = {"task": (116, 66), "event": (36, 36), "gateway": (50, 50)}
TASKS = {"task", "userTask", "serviceTask", "manualTask"}
EVENTS = {"start", "startMessage", "end", "endError"}
GATEWAYS = {"xor", "and"}
BPMN_TAG = {"task": "task", "userTask": "userTask", "serviceTask": "serviceTask", "manualTask": "manualTask",
            "start": "startEvent", "startMessage": "startEvent", "end": "endEvent", "endError": "endEvent",
            "xor": "exclusiveGateway", "and": "parallelGateway"}


def _kind(t: str) -> str:
    return "task" if t in TASKS else ("event" if t in EVENTS else "gateway")


def layout(proc: dict) -> dict:
    lanes = [lane[0] for lane in proc["lanes"]]
    nodes = {}
    for n in proc["nodes"]:
        nid, ntype, lane, col, label = n[:5]
        row = n[5] if len(n) > 5 and n[5] is not None else 0
        badge = n[6] if len(n) > 6 else None
        w, h = SIZE[_kind(ntype)]
        cx = LEFT + 40 + col * COL_W + COL_W / 2
        cy = TOP + lanes.index(lane) * LANE_H + LANE_H / 2 + row * ROW_DY
        nodes[nid] = {"id": nid, "type": ntype, "lane": lane, "label": label, "badge": badge, "cx": cx, "cy": cy, "w": w, "h": h,
                      "x": cx - w / 2, "y": cy - h / 2}
    max_col = max(n[3] for n in proc["nodes"])
    width = LEFT + 40 + (max_col + 1) * COL_W + 20
    height = TOP + len(lanes) * LANE_H + 20
    edges = []
    for i, (src, dst, label) in enumerate(proc["flows"]):
        edges.append({"id": f"f{i + 1}", "src": src, "dst": dst, "label": label, "points": _route(nodes[src], nodes[dst], height)})
    return {"nodes": nodes, "edges": edges, "width": width, "height": height, "lanes": proc["lanes"]}


def _route(a: dict, b: dict, height: float) -> list[tuple[float, float]]:
    ax_r, bx_l = a["cx"] + a["w"] / 2, b["cx"] - b["w"] / 2
    if b["cx"] <= a["cx"]:  # back loop: under both nodes
        low = max(a["cy"] + a["h"] / 2, b["cy"] + b["h"] / 2) + 26
        return [(a["cx"], a["cy"] + a["h"] / 2), (a["cx"], low), (b["cx"], low), (b["cx"], b["cy"] + b["h"] / 2)]
    if abs(a["cy"] - b["cy"]) < 1:
        return [(ax_r, a["cy"]), (bx_l, b["cy"])]
    if a["type"] in GATEWAYS:  # leave the gateway through its top or bottom corner
        sy = a["cy"] - a["h"] / 2 if b["cy"] < a["cy"] else a["cy"] + a["h"] / 2
        return [(a["cx"], sy), (a["cx"], b["cy"]), (bx_l, b["cy"])]
    if b["type"] in GATEWAYS:  # enter the gateway through its top or bottom corner
        ey = b["cy"] - b["h"] / 2 if a["cy"] < b["cy"] else b["cy"] + b["h"] / 2
        return [(ax_r, a["cy"]), (b["cx"], a["cy"]), (b["cx"], ey)]
    mid = (ax_r + bx_l) / 2
    return [(ax_r, a["cy"]), (mid, a["cy"]), (mid, b["cy"]), (bx_l, b["cy"])]


def to_bpmn(proc: dict) -> str:
    lay = layout(proc)
    pid = proc["id"].replace("-", "_")
    out = ['<?xml version="1.0" encoding="UTF-8"?>',
           '<bpmn:definitions xmlns:bpmn="http://www.omg.org/spec/BPMN/20100524/MODEL" xmlns:bpmndi="http://www.omg.org/spec/BPMN/20100524/DI" '
           'xmlns:dc="http://www.omg.org/spec/DD/20100524/DC" xmlns:di="http://www.omg.org/spec/DD/20100524/DI" '
           f'id="defs_{pid}" targetNamespace="https://example.org/vaerdal/bpmn" exporter="erpcase/bpmn.py" exporterVersion="1">',
           f'  <bpmn:collaboration id="collab_{pid}">',
           f'    <bpmn:participant id="pool_{pid}" name="{escape(proc["name"])}" processRef="{pid}" />',
           '  </bpmn:collaboration>',
           f'  <bpmn:process id="{pid}" isExecutable="false">',
           f'    <bpmn:laneSet id="lanes_{pid}">']
    for lane_id, lane_name in proc["lanes"]:
        out.append(f'      <bpmn:lane id="lane_{lane_id}" name="{escape(lane_name)}">')
        out += [f'        <bpmn:flowNodeRef>{n["id"]}</bpmn:flowNodeRef>' for n in lay["nodes"].values() if n["lane"] == lane_id]
        out.append('      </bpmn:lane>')
    out.append('    </bpmn:laneSet>')
    incoming = {nid: [e["id"] for e in lay["edges"] if e["dst"] == nid] for nid in lay["nodes"]}
    outgoing = {nid: [e["id"] for e in lay["edges"] if e["src"] == nid] for nid in lay["nodes"]}
    for n in lay["nodes"].values():
        tag = BPMN_TAG[n["type"]]
        out.append(f'    <bpmn:{tag} id="{n["id"]}" name="{escape(n["label"])}">')
        out += [f'      <bpmn:incoming>{f}</bpmn:incoming>' for f in incoming[n["id"]]]
        out += [f'      <bpmn:outgoing>{f}</bpmn:outgoing>' for f in outgoing[n["id"]]]
        if n["type"] == "startMessage":
            out.append(f'      <bpmn:messageEventDefinition id="med_{n["id"]}" />')
        if n["type"] == "endError":
            out.append(f'      <bpmn:errorEventDefinition id="eed_{n["id"]}" />')
        out.append(f'    </bpmn:{tag}>')
    for e in lay["edges"]:
        name = f' name="{escape(e["label"])}"' if e["label"] else ""
        out.append(f'    <bpmn:sequenceFlow id="{e["id"]}" sourceRef="{e["src"]}" targetRef="{e["dst"]}"{name} />')
    out.append('  </bpmn:process>')
    out.append(f'  <bpmndi:BPMNDiagram id="diagram_{pid}">')
    out.append(f'    <bpmndi:BPMNPlane id="plane_{pid}" bpmnElement="collab_{pid}">')
    out.append(f'      <bpmndi:BPMNShape id="pool_{pid}_di" bpmnElement="pool_{pid}" isHorizontal="true"><dc:Bounds x="{LEFT - 40}" y="{TOP}" width="{lay["width"] - LEFT + 20}" height="{len(proc["lanes"]) * LANE_H}" /></bpmndi:BPMNShape>')
    for i, (lane_id, _) in enumerate(proc["lanes"]):
        out.append(f'      <bpmndi:BPMNShape id="lane_{lane_id}_di" bpmnElement="lane_{lane_id}" isHorizontal="true"><dc:Bounds x="{LEFT - 10}" y="{TOP + i * LANE_H}" width="{lay["width"] - LEFT - 10}" height="{LANE_H}" /></bpmndi:BPMNShape>')
    for n in lay["nodes"].values():
        marker = ' isMarkerVisible="true"' if n["type"] == "xor" else ""
        out.append(f'      <bpmndi:BPMNShape id="{n["id"]}_di" bpmnElement="{n["id"]}"{marker}><dc:Bounds x="{n["x"]:.0f}" y="{n["y"]:.0f}" width="{n["w"]}" height="{n["h"]}" /></bpmndi:BPMNShape>')
    for e in lay["edges"]:
        out.append(f'      <bpmndi:BPMNEdge id="{e["id"]}_di" bpmnElement="{e["id"]}">')
        out += [f'        <di:waypoint x="{x:.0f}" y="{y:.0f}" />' for x, y in e["points"]]
        out.append('      </bpmndi:BPMNEdge>')
    out += ['    </bpmndi:BPMNPlane>', '  </bpmndi:BPMNDiagram>', '</bpmn:definitions>', '']
    return "\n".join(out)


def _wrap(text: str, width: int = 17) -> list[str]:
    lines, cur = [], ""
    for word in text.split():
        if cur and len(cur) + 1 + len(word) > width:
            lines.append(cur)
            cur = word
        else:
            cur = f"{cur} {word}".strip()
    if cur:
        lines.append(cur)
    return lines


def to_svg(proc: dict) -> str:
    lay = layout(proc)
    asis = proc.get("kind") == "asis"
    badge_fill = "#a3312a" if asis else "#1f4e79"
    w, h = lay["width"], lay["height"]
    s = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w:.0f} {h:.0f}" width="{w:.0f}" height="{h:.0f}" role="img" aria-label="{escape(proc["name"])}" font-family="ui-sans-serif, system-ui, -apple-system, Segoe UI, Roboto, Arial, sans-serif">',
         '<defs><marker id="arr" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse"><path d="M0,0 L10,5 L0,10 z" fill="#3b4654"/></marker></defs>',
         f'<rect x="0" y="0" width="{w:.0f}" height="{h:.0f}" fill="#ffffff"/>',
         f'<rect x="{LEFT - 40}" y="{TOP}" width="{w - LEFT + 20:.0f}" height="{len(lay["lanes"]) * LANE_H}" fill="none" stroke="#3b4654" stroke-width="1.2"/>',
         f'<text x="{LEFT - 22}" y="{TOP + len(lay["lanes"]) * LANE_H / 2:.0f}" font-size="13" font-weight="700" fill="#1b2430" text-anchor="middle" transform="rotate(-90 {LEFT - 22} {TOP + len(lay["lanes"]) * LANE_H / 2:.0f})">Vaerdal Foods</text>']
    for i, (_, lane_name) in enumerate(lay["lanes"]):
        y = TOP + i * LANE_H
        s.append(f'<rect x="{LEFT - 10}" y="{y}" width="{w - LEFT - 10:.0f}" height="{LANE_H}" fill="{"#f7f8fa" if i % 2 else "#ffffff"}" stroke="#c9d1db"/>')
        s.append(f'<text x="{LEFT + 6}" y="{y + LANE_H / 2:.0f}" font-size="12" fill="#3b4654" text-anchor="middle" transform="rotate(-90 {LEFT + 6} {y + LANE_H / 2:.0f})">{escape(lane_name)}</text>')
    for e in lay["edges"]:
        pts = " ".join(f"{x:.0f},{y:.0f}" for x, y in e["points"])
        s.append(f'<polyline points="{pts}" fill="none" stroke="#3b4654" stroke-width="1.4" marker-end="url(#arr)"/>')
        if e["label"]:
            (x1, y1), (x2, y2) = e["points"][0], e["points"][1]
            lx, ly = (x1 + 6, (y1 + y2) / 2) if abs(x1 - x2) < 1 else ((x1 + x2) / 2, y1 - 6)
            anchor = "start" if abs(x1 - x2) < 1 else "middle"
            s.append(f'<text x="{lx:.0f}" y="{ly:.0f}" font-size="11" fill="#5b6675" text-anchor="{anchor}">{escape(e["label"])}</text>')
    for n in lay["nodes"].values():
        cx, cy = n["cx"], n["cy"]
        if n["type"] in TASKS:
            s.append(f'<rect x="{n["x"]:.0f}" y="{n["y"]:.0f}" width="{n["w"]}" height="{n["h"]}" rx="9" fill="#ffffff" stroke="#1b2430" stroke-width="1.3"/>')
            ix, iy = n["x"] + 10, n["y"] + 10
            if n["type"] == "userTask":
                s.append(f'<circle cx="{ix:.0f}" cy="{iy - 2:.0f}" r="3" fill="none" stroke="#5b6675"/><path d="M{ix - 5:.0f},{iy + 6:.0f} q5,-8 10,0" fill="none" stroke="#5b6675"/>')
            elif n["type"] == "serviceTask":
                s.append(f'<circle cx="{ix:.0f}" cy="{iy:.0f}" r="5" fill="none" stroke="#5b6675" stroke-width="2.4" stroke-dasharray="2 1.6"/><circle cx="{ix:.0f}" cy="{iy:.0f}" r="1.6" fill="#5b6675"/>')
            elif n["type"] == "manualTask":
                s.append(f'<rect x="{ix - 5:.0f}" y="{iy - 4:.0f}" width="10" height="8" rx="2" fill="none" stroke="#5b6675"/>')
            lines = _wrap(n["label"])
            for j, line in enumerate(lines):
                s.append(f'<text x="{cx:.0f}" y="{cy - (len(lines) - 1) * 6.5 + j * 13 + 4:.0f}" font-size="11" fill="#1b2430" text-anchor="middle">{escape(line)}</text>')
        elif n["type"] in EVENTS:
            end = n["type"].startswith("end")
            s.append(f'<circle cx="{cx:.0f}" cy="{cy:.0f}" r="18" fill="#ffffff" stroke="#1b2430" stroke-width="{3.2 if end else 1.4}"/>')
            if n["type"] == "startMessage":
                s.append(f'<rect x="{cx - 9:.0f}" y="{cy - 6:.0f}" width="18" height="12" fill="none" stroke="#1b2430"/><polyline points="{cx - 9:.0f},{cy - 6:.0f} {cx:.0f},{cy + 1:.0f} {cx + 9:.0f},{cy - 6:.0f}" fill="none" stroke="#1b2430"/>')
            if n["type"] == "endError":
                s.append(f'<polyline points="{cx - 8:.0f},{cy + 7:.0f} {cx - 3:.0f},{cy - 7:.0f} {cx + 3:.0f},{cy + 2:.0f} {cx + 8:.0f},{cy - 8:.0f}" fill="none" stroke="#1b2430" stroke-width="1.6"/>')
            for j, line in enumerate(_wrap(n["label"], 18)):
                s.append(f'<text x="{cx:.0f}" y="{cy + 32 + j * 12:.0f}" font-size="11" fill="#1b2430" text-anchor="middle">{escape(line)}</text>')
        else:
            s.append(f'<polygon points="{cx:.0f},{cy - 25:.0f} {cx + 25:.0f},{cy:.0f} {cx:.0f},{cy + 25:.0f} {cx - 25:.0f},{cy:.0f}" fill="#ffffff" stroke="#1b2430" stroke-width="1.3"/>')
            mark = "×" if n["type"] == "xor" else "+"
            s.append(f'<text x="{cx:.0f}" y="{cy + 7:.0f}" font-size="20" fill="#1b2430" text-anchor="middle">{mark}</text>')
            if n["label"]:
                s.append(f'<text x="{cx - 20:.0f}" y="{cy - 22:.0f}" font-size="11" fill="#1b2430" text-anchor="end">{escape(n["label"])}</text>')
        if n["badge"]:
            bx, by = n["x"] + n["w"] - 2, n["y"] + 2
            s.append(f'<circle cx="{bx:.0f}" cy="{by:.0f}" r="10" fill="{badge_fill}"/><text x="{bx:.0f}" y="{by + 4:.0f}" font-size="11" font-weight="700" fill="#ffffff" text-anchor="middle">{escape(n["badge"])}</text>')
    s.append("</svg>")
    return "\n".join(s) + "\n"
