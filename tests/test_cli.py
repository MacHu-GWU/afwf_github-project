# -*- coding: utf-8 -*-

import json
import pytest
import afwf.api as afwf

from afwf_github.cli import Command
from afwf_github.paths import path_enum


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

@pytest.fixture()
def config_file(tmp_path):
    """Write a minimal valid config.json to tmp_path and return its path."""
    p = tmp_path / "config.json"
    p.write_text(json.dumps({"pac_token": "test-token"}))
    return str(p)


def make_cmd(config_file: str) -> Command:
    return Command(config_file=config_file)


# ---------------------------------------------------------------------------
# require_config decorator
# ---------------------------------------------------------------------------

class TestRequireConfig:
    def test_missing_config_file_returns_error_item(self, tmp_path, monkeypatch):
        captured = []
        monkeypatch.setattr(afwf.ScriptFilter, "send_feedback", lambda self: captured.append(self))

        missing = str(tmp_path / "does_not_exist.json")
        cmd = Command(config_file=missing)
        cmd.view_in_browser(path="")  # path doesn't matter — decorator fires first

        assert len(captured) == 1
        sf = captured[0]
        assert len(sf.items) == 1
        item = sf.items[0]
        assert "Config not found" in item.title
        assert item.variables.get("open_url") == "y"

    def test_valid_config_file_passes_through(self, config_file, monkeypatch):
        captured = []
        monkeypatch.setattr(afwf.ScriptFilter, "send_feedback", lambda self: captured.append(self))

        cmd = make_cmd(config_file)
        cmd.view_in_browser(path="")  # empty path → prompt item (not config error)

        assert len(captured) == 1
        sf = captured[0]
        assert "Config not found" not in sf.items[0].title


# ---------------------------------------------------------------------------
# view_in_browser
# ---------------------------------------------------------------------------

class TestViewInBrowser:
    def test_empty_path_shows_prompt(self, config_file, monkeypatch):
        captured = []
        monkeypatch.setattr(afwf.ScriptFilter, "send_feedback", lambda self: captured.append(self))

        make_cmd(config_file).view_in_browser(path="")

        sf = captured[0]
        assert len(sf.items) == 1
        assert "path" in sf.items[0].title.lower() or "directory" in sf.items[0].title.lower()
        assert sf.items[0].valid is not False  # prompt item should be selectable

    def test_whitespace_only_path_shows_prompt(self, config_file, monkeypatch):
        captured = []
        monkeypatch.setattr(afwf.ScriptFilter, "send_feedback", lambda self: captured.append(self))

        make_cmd(config_file).view_in_browser(path="   ")

        sf = captured[0]
        assert len(sf.items) == 1
        assert "Config not found" not in sf.items[0].title

    def test_git_repo_path_returns_github_url(self, config_file, monkeypatch):
        captured = []
        monkeypatch.setattr(afwf.ScriptFilter, "send_feedback", lambda self: captured.append(self))

        # Use the project root — it's a git repo on GitHub
        make_cmd(config_file).view_in_browser(path=str(path_enum.dir_project_root))

        sf = captured[0]
        assert len(sf.items) == 1
        item = sf.items[0]
        assert "github.com" in item.subtitle
        assert item.variables.get("open_url") == "y"
        assert "github.com" in item.variables.get("open_url_arg", "")

    def test_specific_file_returns_github_url(self, config_file, monkeypatch):
        captured = []
        monkeypatch.setattr(afwf.ScriptFilter, "send_feedback", lambda self: captured.append(self))

        # Use this test file itself — also inside the git repo
        make_cmd(config_file).view_in_browser(path=str(path_enum.dir_project_root / "pyproject.toml"))

        sf = captured[0]
        item = sf.items[0]
        assert "github.com" in item.subtitle
        assert "pyproject.toml" in item.variables.get("open_url_arg", "")

    def test_non_git_path_returns_error_item(self, config_file, monkeypatch, tmp_path):
        captured = []
        monkeypatch.setattr(afwf.ScriptFilter, "send_feedback", lambda self: captured.append(self))

        # tmp_path is outside any git repo
        make_cmd(config_file).view_in_browser(path=str(tmp_path))

        sf = captured[0]
        assert len(sf.items) == 1
        item = sf.items[0]
        assert item.valid is False
        assert "git" in item.title.lower()


if __name__ == "__main__":
    from afwf_github.tests import run_cov_test

    run_cov_test(
        __file__,
        "afwf_github.cli",
        preview=False,
    )
