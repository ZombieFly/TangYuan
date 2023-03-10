from utils import PrintWithoutHide


class TYException(Exception):
    def __init__(self, exp: Exception):
        self.exp = exp
        try:
            getattr(self, exp.__class__.__name__)(exp)
        except Exception:
            self.Exception(exp)

    def OSError(self, exp: OSError):
        with PrintWithoutHide(exp.args[0]):
            pass

    def ValueError(self, exp: ValueError):
        with PrintWithoutHide():
            print("Success, but clipboard is not contain html.")

    def ImportError(self, exp: ImportError):
        with PrintWithoutHide():
            print("Module missing, please check file integrity.")

    def Exception(self, exp: Exception):
        with PrintWithoutHide(repr(exp)):
            pass
