from app.graph.routers import validation_router, has_more_sections_router
from app.graph.nodes.retry_nodes import increment_retry_count


def test_validation_router_passed():
    state = {"validation_status": "passed", "retry_count": 0, "max_retries": 2}
    assert validation_router(state) == "store"


def test_validation_router_skip():
    state = {"validation_status": "skip", "retry_count": 0, "max_retries": 2}
    assert validation_router(state) == "store"


def test_validation_router_retry():
    state = {"validation_status": "retry", "retry_count": 0, "max_retries": 2}
    assert validation_router(state) == "retry"


def test_validation_router_retry_exceeded():
    state = {"validation_status": "retry", "retry_count": 2, "max_retries": 2}
    assert validation_router(state) == "store"


def test_has_more_sections_continue():
    state = {
        "current_section_index": 1,
        "section_names": ["A", "B", "C"]
    }

    assert has_more_sections_router(state) == "continue"


def test_has_more_sections_end():
    state = {
        "current_section_index": 3,
        "section_names": ["A", "B", "C"]
    }

    assert has_more_sections_router(state) == "end"


def test_increment_retry_count():
    state = {"retry_count": 1}

    result = increment_retry_count(state)

    assert result["retry_count"] == 2
    assert result["current_step"] == "retry_count_incremented"