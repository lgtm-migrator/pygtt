from pygtt import Stop, Bus
from datetime import datetime


def test_stop():
    stop = Stop("1234", [])
    assert stop.name == "1234"
    assert stop.bus_list == []
    assert stop.next is None


def test_stop_next():
    stop = Stop(
        "1234",
        [
            Bus("1", [datetime.fromtimestamp(1237), datetime.fromtimestamp(1236)]),
            Bus("2", [datetime.fromtimestamp(1235), datetime.fromtimestamp(1234)]),
        ],
    )
    assert stop.next.name == "2"
    assert stop.next.first_time == datetime.fromtimestamp(1234)
