import pytest

from dag.executors import NOT_AVAILABLE
from dag.graph import DAG
from dag.serialization import deserialize


@pytest.mark.parametrize(
    "params, expected",
    [
        (
            {
                "D": 1,
                "E": 2,
                "F": 3,
                "G": 4,
            },
            [5],
        ),
        (
            {
                "D": 52345,
                "E": 12312,
                "F": 66331,
                "G": 74326,
            },
            [86638],
        ),
        (
            {},
            ["N/A"],
        ),
    ],
)
def test_evaluate_example_graph(params, expected, resources):
    nodes, edges = deserialize(resources / "example_1.xml")

    dag = DAG()
    dag.initialize(nodes, edges)

    result = dag.evaluate(params)

    assert expected == result


@pytest.mark.parametrize(
    "params, expected",
    [
        (
            {
                "D": 1,
                "E": 2,
                "F": 3,
                "G": 4,
            },
            [NOT_AVAILABLE],
        )
    ],
)
def test_evaluate_example_with_exception_graph(params, expected, resources):
    nodes, edges = deserialize(resources / "example_with_exception.xml")

    dag = DAG()
    dag.initialize(nodes, edges)

    result = dag.evaluate(params)

    assert expected == result
