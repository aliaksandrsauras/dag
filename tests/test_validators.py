import pytest

from dag.graph import DAG
from dag.serialization import deserialize


@pytest.mark.parametrize(
    "graph_path",
    [
        "example_1.xml",
        "example_2.xml",
        "example_with_exception.xml",
    ],
)
def test_validate_valid_graphs(resources, graph_path):
    nodes, edges = deserialize(resources / graph_path)

    dag = DAG()
    dag.initialize(nodes, edges)

    is_valid, _ = dag.validate()

    assert is_valid is True


@pytest.mark.parametrize(
    "graph_path",
    [
        "not_valid/cycled_1.xml",
        "not_valid/cycled_2.xml",
        "not_valid/disconnected_1.xml",
        "not_valid/disconnected_2.xml",
        "not_valid/single.xml",
    ],
)
def test_validate_not_valid_graphs(resources, graph_path):
    nodes, edges = deserialize(resources / graph_path)

    dag = DAG()
    dag.initialize(nodes, edges)

    is_valid, _ = dag.validate()

    assert is_valid is False
