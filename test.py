from sqlalchemy.orm import sessionmaker

from db.mange_db import _create_engine
from db.modle import SESSION_LOGIN

_session = sessionmaker(
    bind=_create_engine(),
    autocommit=False,
    autoflush=False
)()

rows = _session.query(SESSION_LOGIN).all()

for row in rows:
    print(
        f"email={row.email!r}, "
        f"session_id={row.session_id!r}"
    )