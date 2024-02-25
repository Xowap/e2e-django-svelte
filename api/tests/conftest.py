import fcntl
import os
import re
import select
import subprocess
import time
from pathlib import Path

import httpx
import pytest
from django.conf import settings
from strip_ansi import strip_ansi


@pytest.fixture(scope="session")
def front_dir() -> Path:
    """Location of the front-end source code"""

    return settings.BASE_DIR / ".." / "front"


@pytest.fixture(scope="session")
def vite_path(front_dir: Path) -> Path:
    """Location of the vite binary"""

    return front_dir / "node_modules/.bin/vite"


@pytest.fixture(scope="session")
def front_env(live_server):
    """
    Environment variables to be injected into the front

    Notes
    -----
    Apparently "localhost" is translated on GHA as "::1" however the live
    server only listens on IPv4 (grrr) so we need to force the use of 127.0.0.1
    in order for this thing to work.
    """

    target_url = httpx.URL(live_server.url)

    if target_url.host == "localhost":
        target_url = target_url.copy_with(host="127.0.0.1")

    return dict(
        API_URL=str(target_url),
    )


@pytest.fixture(scope="session")
def front_build(front_dir: Path, vite_path: Path, front_env) -> None:
    """Builds the front-end"""

    subprocess.run(
        [vite_path, "build"],
        cwd=front_dir,
        check=True,
        env={**os.environ, **front_env},
    )


@pytest.fixture(scope="session")
def front_server(front_build: None, front_dir: Path, vite_path: Path, front_env):
    """Starts the front-end on a random port until the fixture isn't required
    anymore. The returned value is the base URL of that running front-end."""

    with subprocess.Popen(
        [vite_path, "preview", "--port", "0"],
        cwd=front_dir,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        stdin=subprocess.DEVNULL,
        text=True,
        env={**os.environ, **front_env},
    ) as p:
        for stream in [p.stdout, p.stderr]:
            fd = stream.fileno()
            fl = fcntl.fcntl(fd, fcntl.F_GETFL)
            fcntl.fcntl(fd, fcntl.F_SETFL, fl | os.O_NONBLOCK)

        server_address = None
        total_timeout = 5
        start_time = time.time()
        output = {"stdout": "", "stderr": ""}

        try:
            while not server_address:
                remaining_time = total_timeout - (time.time() - start_time)

                if remaining_time <= 0:
                    raise TimeoutError(
                        f"Server did not start within the given timeout. "
                        f"Stdout: {output['stdout']} Stderr: {output['stderr']}"
                    )

                ready, _, _ = select.select(
                    [p.stdout, p.stderr], [], [], remaining_time
                )

                for stream in ready:
                    try:
                        line = stream.readline()
                        if stream is p.stdout:
                            output["stdout"] += line
                        else:
                            output["stderr"] += line
                    except IOError:
                        continue

                    if stream is p.stdout and line:
                        if match := re.search(r"https?://[^/]+/", line):
                            server_address = match.group(0)
                            break
                    elif not line:
                        break

            yield strip_ansi(server_address)

        except Exception as e:
            raise Exception(
                f"Failed to start the server: {str(e)} "
                f"Stdout: {output['stdout']} Stderr: {output['stderr']}"
            )
        finally:
            p.terminate()
