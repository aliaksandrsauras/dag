import itertools


class Color:
    WHITE = 0
    GRAY = 1
    BLACK = 2


class State:
    def __init__(self):
        self.has_cycle = False


class DAGValidator:
    def validate(self, nodes):
        issues = []
        if len(nodes) <= 1:
            issues.append("Graph must have at least two nodes")

        if not self._is_acycle(nodes):
            issues.append("Graph must be acycled")

        if not self._is_connected(nodes):
            issues.append("Graph must be connected")

        return not bool(issues), issues

    def _is_acycle(self, nodes):
        colors = {n.node_id: Color.WHITE for n in nodes.values()}
        state = State()

        for node in nodes.values():
            if colors[node.node_id] == Color.WHITE:
                self._is_acycle_dfs(nodes, node, colors, state)
            if state.has_cycle:
                break

        return not state.has_cycle

    def _is_acycle_dfs(self, nodes, node, colors, state):
        colors[node.node_id] = Color.GRAY

        for n in nodes[node.node_id].outs:
            if colors[n.node_id] == Color.GRAY:
                state.has_cycle = True
                return
            if colors[n.node_id] == Color.WHITE:
                self._is_acycle_dfs(nodes, n, colors, state)

        colors[node.node_id] = Color.BLACK

    def _is_connected(self, nodes):
        colors = {n.node_id: Color.WHITE for n in nodes.values()}

        node = next(iter(nodes.values()))
        visited_nodes = self._is_connected_dfs(node, colors)

        is_connected = visited_nodes == len(nodes)
        return is_connected

    def _is_connected_dfs(self, node, colors):
        visited_nodes = 1
        colors[node.node_id] = Color.GRAY

        for n in itertools.chain(node.ins, node.outs):
            if not colors[n.node_id] == Color.GRAY:
                visited_nodes += self._is_connected_dfs(n, colors)

        return visited_nodes
