# Evaluation of a connected directed acyclic graph

[![Actions](https://github.com/avsavras/dag/actions/workflows/ci.yml/badge.svg)](https://github.com/avsavras/dag/actions?workflow=ci)

## Getting started

The project contains a python package for evaluating pre-prepared graphs, provided in an xml-based format (GraphML).

[Entry point script with example](tests/run_dag_evaluation.py)

[Pre-prepared graphs](resources)

### Simple graph description example

```xml

<graph>
    <node id="A" operator="sum"/>
    <node id="B" operator="min"/>
    <node id="C" operator="max"/>
    <node id="D"/>
    <node id="E"/>
    <node id="F"/>
    <node id="G"/>
    <edge source="B" target="A"/>
    <edge source="C" target="A"/>
    <edge source="D" target="B"/>
    <edge source="E" target="B"/>
    <edge source="F" target="C"/>
    <edge source="G" target="C"/>
</graph>
```

### Simple usage example

```python
from dag.graph import DAG
from dag.serialization import deserialize

nodes, edges = deserialize("resources/example.xml")
params = {"D": 1, "E": 2, "F": 3, "G": 4}

dag = DAG()
dag.initialize(nodes, edges)

is_valid, _ = dag.validate()

if is_valid:
    print(dag.evaluate(params))
```

## Requirements

* Python 3.9+
