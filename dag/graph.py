import logging
import queue
from typing import Optional

from dag.executors import ThreadedExecutor
from dag.operators import OPERATORS
from dag.validators import DAGValidator

logger = logging.getLogger(__name__)

NODES_TYPE = list[tuple[str, Optional[str]]]
EDGES_TYPE = list[tuple[str, str]]
PARAMS_TYPE = dict[str, int]

BAD_EDGE = "Failed to create an edge. The node with the ID '%s' does not exist in the graph"
BAD_PARAM = "Failed to set a param '%s'. Node with the ID: '%s' does not exist in the graph"

BAD_NODE_TYPE = "The node ID must be type of str, given '%s'"
BAD_PARAM_TYPE = "The param must be type of int, given '%s'"


class Node:
    def __init__(self, node_id: str, operator=None):
        self.node_id = node_id
        self.ins: list[Node] = []
        self.outs: list[Node] = []
        self.operator = operator
        self.evaluated_ins = 0
        self.value = None

    def flush(self):
        self.evaluated_ins = 0
        self.value = None


class DAG:
    def __init__(self):
        self.nodes: dict[str, Node] = {}
        self.outputs = []

        # Executor and Validator can be injected for more flexibility and testability
        # By default, the level of parallelism for executor is determined automatically
        self.validator = DAGValidator()
        self.executor = ThreadedExecutor()

    def initialize(self, nodes: NODES_TYPE, edges: EDGES_TYPE):
        self._add_nodes(nodes)
        self._add_edges(edges)

        for node in self.nodes.values():
            if not node.outs:
                self.outputs.append(node)

    def validate(self) -> tuple[bool, list]:
        return self.validator.validate(self.nodes)

    def evaluate(self, params: PARAMS_TYPE):
        self._set_params(params)

        inputs = queue.Queue()

        for node in self.nodes.values():
            if not node.ins:
                inputs.put(node)

        self.executor.execute(inputs)
        result = [node.value for node in self.outputs]
        self._flush()
        return result

    def _flush(self):
        for node in self.nodes.values():
            node.flush()

    def _add_nodes(self, nodes: NODES_TYPE):
        # Unknown operators are automatically converted to None, this is considered as a valid case
        for node_id, operator in nodes:
            self.nodes[node_id] = Node(node_id, OPERATORS.get(operator, None))

    def _add_edges(self, edges: EDGES_TYPE):
        for src_id, dst_id in edges:
            assert src_id in self.nodes, BAD_EDGE % src_id
            assert dst_id in self.nodes, BAD_EDGE % dst_id
            src = self.nodes[src_id]
            dst = self.nodes[dst_id]
            dst.ins.append(src)
            src.outs.append(dst)

    def _set_params(self, params: PARAMS_TYPE):
        for node_id, param in params.items():
            assert isinstance(node_id, str), BAD_NODE_TYPE % type(node_id)
            assert isinstance(param, int), BAD_PARAM_TYPE % type(param)
            assert node_id in self.nodes, BAD_PARAM % (param, node_id)
            self.nodes[node_id].value = param
