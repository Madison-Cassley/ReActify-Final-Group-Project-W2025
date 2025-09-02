import contextlib
import sys
from pathlib import Path

if not __package__:
    # Make CLI runnable from source tree with
    #    python src/package
    # See: https://packaging.python.org/en/latest/discussions/src-layout-vs-flat-layout/#running-a-command-line-interface-from-source-with-src-layout
    package_source_path = Path(__file__).parent.parent.as_posix()
    sys.path.insert(0, package_source_path)


if __name__ == "__main__":
    from runner import main

    with contextlib.suppress(KeyboardInterrupt):
        main()
