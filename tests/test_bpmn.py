"""The BPMN files are valid BPMN 2.0 with diagram interchange."""
import json
import unittest
import xml.etree.ElementTree as ET

from erpcase import bpmn

from .helpers import ROOT

NS = {"bpmn": "http://www.omg.org/spec/BPMN/20100524/MODEL", "bpmndi": "http://www.omg.org/spec/BPMN/20100524/DI"}
FLOW_NODES = ["startEvent", "endEvent", "task", "userTask", "serviceTask", "manualTask", "exclusiveGateway", "parallelGateway"]


class Bpmn(unittest.TestCase):
    def setUp(self):
        self.processes = json.loads((ROOT / "data/processes.json").read_text(encoding="utf-8"))["processes"]

    def test_files_match_the_definitions(self):
        for proc in self.processes:
            with self.subTest(proc=proc["id"]):
                on_disk = (ROOT / f"docs/03-processen/bpmn/{proc['id']}.bpmn").read_text(encoding="utf-8")
                self.assertEqual(on_disk, bpmn.to_bpmn(proc))

    def test_structure(self):
        for proc in self.processes:
            with self.subTest(proc=proc["id"]):
                root = ET.fromstring(bpmn.to_bpmn(proc))
                process = root.find("bpmn:process", NS)
                nodes = {el.get("id"): el for tag in FLOW_NODES for el in process.findall(f"bpmn:{tag}", NS)}
                flows = process.findall("bpmn:sequenceFlow", NS)
                self.assertTrue(process.findall("bpmn:startEvent", NS))
                self.assertTrue(process.findall("bpmn:endEvent", NS))
                for f in flows:
                    self.assertIn(f.get("sourceRef"), nodes)
                    self.assertIn(f.get("targetRef"), nodes)
                in_lanes = [ref.text for lane in process.iter(f"{{{NS['bpmn']}}}lane") for ref in lane.findall("bpmn:flowNodeRef", NS)]
                self.assertEqual(sorted(in_lanes), sorted(nodes))  # every node in exactly one lane
                shapes = {s.get("bpmnElement") for s in root.iter(f"{{{NS['bpmndi']}}}BPMNShape")}
                edges = {e.get("bpmnElement") for e in root.iter(f"{{{NS['bpmndi']}}}BPMNEdge")}
                self.assertLessEqual(set(nodes), shapes)
                self.assertEqual({f.get("id") for f in flows}, edges)
                for node_id, el in nodes.items():
                    tag = el.tag.split("}")[1]
                    if tag != "startEvent":
                        self.assertTrue(el.findall("bpmn:incoming", NS), f"{node_id} has no incoming flow")
                    if tag != "endEvent":
                        self.assertTrue(el.findall("bpmn:outgoing", NS), f"{node_id} has no outgoing flow")
                    if tag == "exclusiveGateway":
                        self.assertTrue(len(el.findall("bpmn:incoming", NS)) > 1 or len(el.findall("bpmn:outgoing", NS)) > 1)

    def test_badges_have_notes(self):
        for proc in self.processes:
            badges = {n[6] for n in proc["nodes"] if len(n) > 6 and n[6]}
            notes = {n[0] for n in proc.get("notes", [])}
            self.assertEqual(badges, notes, proc["id"])


if __name__ == "__main__":
    unittest.main()
