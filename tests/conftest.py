import os
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
# the API lives in backend/ (src.main:backend_app)
for p in (ROOT / "backend",):
    if str(p) not in sys.path:
        sys.path.insert(0, str(p))

# Keep test data and the SQLite file out of the repo.
_tmp = tempfile.mkdtemp(prefix="leads-tests-")
os.environ["DATA_DIR"] = _tmp
os.environ["DATABASE_URL"] = f"sqlite+aiosqlite:///{Path(_tmp, 'app.db').as_posix()}"
