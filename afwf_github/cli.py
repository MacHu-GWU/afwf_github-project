# -*- coding: utf-8 -*-

import sys
import json
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

_CONFIG_TEMPLATE = {
    "pac_token": None,
    "pac_token_home_secret_toml_path": None,
    "cache_expire": 2_592_000,
}

_log_error = afwf.log_error(
    log_file=path_enum.path_error_log,
    tb_limit=10,
)


def _error_sf(exc: Exception) -> afwf.ScriptFilter:
    item = afwf.Item(
        title=f"{type(exc).__name__}: {exc}",
        subtitle=f"Press Enter to open the error log: {path_enum.path_error_log}",
        icon=afwf.Icon.from_image_file(path=afwf.IconFileEnum.error),
        valid=True,
    )
    item.open_file(str(path_enum.path_error_log))
    return afwf.ScriptFilter(items=[item])


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

    @afwf.log_error(

    )
    def edit_config(self) -> None:
        """Script Filter: open config.json in the default editor.

        Creates a blank template at the default path if the file does not yet
        exist, then opens it via Alfred's Open File action.

        Alfred Script field (dev):
            .venv/bin/afwf-github edit-config

        Alfred Script field (prod):
            ~/.local/bin/uvx --from afwf_github==<ver> afwf-github edit-config
        """
        @_log_error
        def _run():
            config_path = path_enum.path_config_json
            if not config_path.exists():
                config_path.parent.mkdir(parents=True, exist_ok=True)
                config_path.write_text(json.dumps(_CONFIG_TEMPLATE, indent=4))
            item = afwf.Item(
                title="Open and edit config.json",
                subtitle=str(config_path),
                icon=afwf.Icon.from_image_file(path=afwf.IconFileEnum.file),
            )
            item.open_file(str(config_path))
            afwf.ScriptFilter(items=[item]).send_feedback()

        try:
            _run()
        except Exception as e:
            _error_sf(e).send_feedback()

    @require_config
    def view_in_browser(self, path: str = "") -> None:
        """Script Filter: given a local file or directory path, open its GitHub URL in the browser.

        Alfred Script field (dev):
            .venv/bin/afwf-github view-in-browser --path '{query}'

        Alfred Script field (prod):
            ~/.local/bin/uvx --from afwf_github==<ver> afwf-github view-in-browser --path '{query}'
        """
        @_log_error
        def _run():
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

        try:
            _run()
        except Exception as e:
            _error_sf(e).send_feedback()

    @require_config
    def search_repo(self, query: str = "") -> None:
        """Script Filter: search GitHub repositories in the local index.

        Alfred Script field (dev):
            .venv/bin/afwf-github search-repo --query '{query}'

        Alfred Script field (prod):
            ~/.local/bin/uvx --from afwf_github==<ver> afwf-github search-repo --query '{query}'
        """
        @_log_error
        def _run():
            if not query.strip():
                afwf.ScriptFilter(
                    items=[afwf.Item(title="Type to search GitHub repositories ...")]
                ).send_feedback()
                return

            dataset = create_repo_dataset(config=self._config)
            repos = dataset.search(query=query, limit=50, simple_response=True, verbose=False)

            if not repos:
                afwf.ScriptFilter(
                    items=[
                        afwf.Item(
                            title=f"No repository found for: {query!r}",
                            icon=afwf.Icon.from_image_file(path=afwf.IconFileEnum.error),
                            valid=False,
                        )
                    ]
                ).send_feedback()
                return

            items = []
            for repo in repos:
                account_name = repo["acc"]
                repo_name = repo["repo"]
                repo_description = repo.get("desc", "No description")
                url = f"https://github.com/{account_name}/{repo_name}"
                item = afwf.Item(
                    title=f"{account_name}/{repo_name}",
                    subtitle=repo_description,
                    autocomplete=f"{account_name}/{repo_name}",
                    icon=afwf.Icon.from_image_file(path=afwf.IconFileEnum.git),
                )
                item.open_url(url)
                items.append(item)
            afwf.ScriptFilter(items=items).send_feedback()

        try:
            _run()
        except Exception as e:
            _error_sf(e).send_feedback()

    @require_config
    def rebuild_index(self) -> None:
        """Script Filter: show a single item that triggers ``rebuild-index-action`` on Enter.

        Alfred Script field (dev):
            .venv/bin/afwf-github rebuild-index

        Alfred Script field (prod):
            ~/.local/bin/uvx --from afwf_github==<ver> afwf-github rebuild-index
        """
        @_log_error
        def _run():
            bin_cli = Path(sys.executable).parent / "afwf-github"
            cmd = f"{bin_cli} rebuild-index-action"
            if self.config_file is not None:
                cmd += f" --config-file {self.config_file!r}"

            item = afwf.Item(
                title="Rebuild Index for GitHub Alfred Workflow",
                subtitle="Hit Enter to rebuild — may take 10–20 seconds",
                icon=afwf.Icon.from_image_file(path=afwf.IconFileEnum.reset),
            )
            item.run_script(cmd)
            afwf.ScriptFilter(items=[item]).send_feedback()

        try:
            _run()
        except Exception as e:
            _error_sf(e).send_feedback()

    @require_config
    @_log_error
    def rebuild_index_action(self) -> None:
        """Rebuild the local repo search index by re-fetching data from GitHub.

        Called by Alfred's Run Script widget — NOT a Script Filter.

        Alfred Run Script field (dev):
            .venv/bin/afwf-github rebuild-index-action

        Alfred Run Script field (prod):
            ~/.local/bin/uvx --from afwf_github==<ver> afwf-github rebuild-index-action
        """
        create_repo_dataset(config=self._config).search(
            query="",
            refresh=True,
        )


def run():
    fire.Fire(Command)
