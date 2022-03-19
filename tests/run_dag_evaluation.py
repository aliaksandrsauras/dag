import logging

from dag.graph import DAG
from dag.logs import init_console_logs_for_module, log_timing
from dag.serialization import deserialize

logger = logging.getLogger(__name__)


@log_timing
def main(params):
    init_console_logs_for_module(__name__)
    init_console_logs_for_module("dag")

    nodes, edges = deserialize("../resources/example_1.xml")

    dag = DAG()
    dag.initialize(nodes, edges)

    is_valid, issues = dag.validate()

    if is_valid:
        result = dag.evaluate(params)
        logger.info("Result of evaluation is %s", result)
    else:
        for i in issues:
            logger.error(i)

        logger.error("Given graph is not a DAG")


if __name__ == "__main__":
    p = {
        "D": 1,
        "E": 2,
        "F": 3,
        "G": 4,
    }

    main(p)
