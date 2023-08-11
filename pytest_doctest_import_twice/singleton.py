import sys
import traceback
from types import TracebackType


def make_tb() -> TracebackType:
    tb = None
    depth = 0
    while True:
        try:
            frame = sys._getframe(depth)
            depth += 1
        except ValueError:
            break

        tb = TracebackType(tb, frame, frame.f_lasti, frame.f_lineno)
    return tb


class MyVindictiveSingleton:
    BOOM = []

    def __init__(self) -> None:
        cls = type(self)
        cls.BOOM.append(make_tb())
        if len(cls.BOOM) > 1:
            sep = "\n-----------------------------------\n\n"
            tbs = ["".join(traceback.format_tb(t)) for t in cls.BOOM]
            msg = f"Already initialized, {sep.join(tbs)}"
            raise RuntimeError(msg)
