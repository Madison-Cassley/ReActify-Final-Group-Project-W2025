import contextlib
import sys
from pathlib import Path

if not __package__:
    package_source_path = Path(__file__).parent.parent.as_posix()
    sys.path.insert(0, package_source_path)

if __name__ == "__main__":
    from earthquake_subsystem.runner import main

    with contextlib.suppress(KeyboardInterrupt):
        main()
