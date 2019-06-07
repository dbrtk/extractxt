
from chardet import UniversalDetector


def run_chardet(detector: UniversalDetector= None, path: str = None) -> dict:

    if not detector:
        detector = UniversalDetector()
    else:
        detector.reset()
    with open(path, 'rb') as _file:
        for _line in _file.readlines():
            detector.feed(_line)
            if detector.done:
                break
    return detector.result

