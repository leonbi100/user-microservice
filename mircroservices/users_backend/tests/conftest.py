import os
import tempfile
import pytest
from ..app import app


# Creates a fixture whose name is "app"
# and returns our flask server instance
@pytest.fixture
def client():
    db_fd, app.config['DATABASE'] = tempfile.mkstemp()
    app.config['TESTING'] = True

    with app.test_client() as client:
        yield client

    os.close(db_fd)
    os.unlink(app.config['DATABASE'])