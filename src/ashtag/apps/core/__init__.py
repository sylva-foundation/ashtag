

# Take a moment to monkey-patch pipeline to make it list
# files in a deterministic order (so we get the same
# output on every server)
from pipeline import glob
_old_glob = glob.glob


def _deterministic_glob(pathname):
        return sorted(_old_glob(pathname))
glob.glob = _deterministic_glob
