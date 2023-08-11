import inspect
import traceback
from types import FrameType, TracebackType


def make_tb(*, skip=0) -> TracebackType:
    tb = None
    frame = inspect.currentframe()
    # skip own frame
    if frame is None:
        raise RuntimeError("Could not skip own frame")
    frame = frame.f_back
    # skip specified frames
    for i in range(skip):
        if frame is None:
            raise RuntimeError(f"Could not skip frame {i+1}/{skip}")
        frame = frame.f_back
    # construct traceback
    while frame is not None:
        tb = TracebackType(tb, frame, frame.f_lasti, frame.f_lineno)
        frame = frame.f_back
    return tb


def find_frame(name: str) -> FrameType | None:
    frame = inspect.currentframe()
    while frame := frame.f_back:  # First needs to be skipped anyway
        if frame.f_code.co_name == name:
            return frame
    return None


class MyVindictiveSingleton:
    BOOM = []

    def __init__(self) -> None:
        cls = type(self)
        cls.BOOM.append(
            dict(
                tb=make_tb(skip=1),
                **find_frame("import_path").f_locals,
            )
        )
        if len(cls.BOOM) > 1:
            sep = "\n-----------------------------------\n\n"
            tbs = [
                f"module_name: {t['module_name']}\n\n{''.join(traceback.format_tb(t['tb']))}"
                for t in cls.BOOM
            ]
            msg = f"Already initialized:\n{sep.join(tbs)}"
            raise RuntimeError(msg)
