"""Fixtures for int01 (BikeMap) tests: a real `loop.mockserver.maps` HTTP server on a
random OS-assigned port, started/stopped per test via `start_in_thread()`."""

from __future__ import annotations

import pytest

from loop.mockserver import maps


@pytest.fixture()
def maps_server():
    """Base URL of a freshly-started maps mockserver; shuts down after the test."""
    server, thread = maps.start_in_thread(port=0)
    base_url = f"http://127.0.0.1:{server.server_address[1]}"
    yield base_url
    server.shutdown()
    server.server_close()
