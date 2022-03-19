from dag.serialization import deserialize


def test_deserialize(resources):
    nodes, edges = deserialize(resources / "example_1.xml")

    expected_nodes = [
        ("A", "sum"),
        ("B", "min"),
        ("C", "max"),
        ("D", None),
        ("E", None),
        ("F", None),
        ("G", None),
    ]
    expected_edges = [
        ("B", "A"),
        ("C", "A"),
        ("D", "B"),
        ("E", "B"),
        ("F", "C"),
        ("G", "C"),
    ]

    assert expected_nodes == nodes
    assert expected_edges == edges
