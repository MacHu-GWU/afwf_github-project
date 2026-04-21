# -*- coding: utf-8 -*-

import typing as T
import functools
from pathlib import Path
from functools import cached_property

import fire
import afwf.api as afwf
import git_web_url.api as gwu
from git_web_url.exc import NotGitRepoError

from .config import Config
from .paths import path_enum
from .dataset import create_repo_dataset


def _config_error_sf(config_path: Path) -> afwf.ScriptFilter:
    item = afwf.Item(
        title=f"Config file not found: {config_path}",
        subtitle="Press Enter to open the setup guide on GitHub",
        icon=afwf.Icon.from_image_file(path=afwf.IconFileEnum.error),
        valid=True,
    )
    item.open_url("https://github.com/MacHu-GWU/afwf_github-project")
    return afwf.ScriptFilter(items=[item])


def require_config(method: T.Callable) -> T.Callable:
    """Decorator that resolves and loads config before calling a CLI method.

    Resolution order:
    1. If ``self.config_file`` is set, load from that path.
    2. Otherwise use the default path (``path_enum.path_config_json``).

    On any failure (file missing, parse error) the decorator outputs a
    single error ``Item`` that opens the project README on Enter, then
    returns early so the wrapped method is never called.

    On success, ``self._config`` is populated and the wrapped method runs
    normally.

    ``functools.wraps`` is still required in Python 3.10+ to copy
    ``__name__``, ``__doc__``, ``__wrapped__``, etc. onto the wrapper —
    ``ParamSpec`` (added in 3.10) improves type-checker inference for
    decorators but does not replace ``functools.wraps``.
    """

    @functools.wraps(method)
    def wrapper(self: "Command", *args, **kwargs):
        if self.config_file is not None:
            config_path = Path(self.config_file).expanduser().resolve()
        else:
            config_path = path_enum.path_config_json

        if not config_path.exists():
            _config_error_sf(config_path).send_feedback()
            return

        try:
            self._config = Config.load(config_path)
        except Exception:
            _config_error_sf(config_path).send_feedback()
            return

        return method(self, *args, **kwargs)

    return wrapper


class Command:
    """Alfred GitHub Workflow CLI.

    All subcommands accept an optional ``--config-file`` argument (absolute
    or relative path).  When omitted, config is loaded from the default
    location via ``default_config``.
    """

    def __init__(self, config_file: str | None = None):
        self.config_file = config_file
        self._config: Config | None = None

    @cached_property
    def default_config(self) -> Config:
        """Load config from the default path (``~/.alfred-afwf/afwf_github/config.json``)."""
        return Config.load(path_enum.path_config_json)

    @require_config
    def view_in_browser(self, path: str = "") -> None:
        """Given a local file or directory path, open its GitHub URL in the browser.

        Alfred Script field (dev):
            .venv/bin/afwf-github view-in-browser --path '{query}'

        Alfred Script field (prod):
            ~/.local/bin/uvx --from afwf_github==<ver> afwf-github view-in-browser --path '{query}'
        """
        if not path.strip():
            afwf.ScriptFilter(
                items=[
                    afwf.Item(
                        title="Type or paste the absolute path of a local file or directory"
                    )
                ]
            ).send_feedback()
            return

        try:
            url = gwu.get_web_url(Path(path))
            item = afwf.Item(
                title=f"Open in browser: {url}",
                subtitle=f"Local path: {path}",
                icon=afwf.Icon.from_image_file(path=afwf.IconFileEnum.internet),
            )
            item.open_url(url)
        except NotGitRepoError:
            item = afwf.Item(
                title=f"Not a git repository path: {path}",
                subtitle="Only paths inside a git repo with a remote can be opened in browser",
                icon=afwf.Icon.from_image_file(path=afwf.IconFileEnum.error),
                valid=False,
            )

        afwf.ScriptFilter(items=[item]).send_feedback()

    @require_config
    def rebuild_index(self) -> None:
        """Rebuild the local repo search index by re-fetching data from GitHub.

        Called by Alfred's Run Script widget — NOT a Script Filter.

        Alfred Run Script field (dev):
            .venv/bin/afwf-github rebuild-index

        Alfred Run Script field (prod):
            ~/.local/bin/uvx --from afwf_github==<ver> afwf-github rebuild-index
        """
        create_repo_dataset(config=self._config).search(
            query="",
            refresh=True,
        )


def run():
    fire.Fire(Command)
