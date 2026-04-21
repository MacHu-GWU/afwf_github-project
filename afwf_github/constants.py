# -*- coding: utf-8 -*-

import enum


class CacheKeyEnum(str, enum.Enum):
    """
    Cache keys for GitHub data, parameterized by GitHub username.

    Each data type is stored under a separate key (``user@{username}``,
    ``accounts@{username}``, ``repos@{username}``) rather than a single
    combined JSON blob. This allows callers to fetch only what they need:
    reading the authenticated user or listing org accounts is cheap and
    instantaneous, while fetching all repositories can be slow for accounts
    with hundreds of repos. Keeping them separate avoids paying the full
    download cost just to answer a lightweight query.
    """

    user = "user"
    """Authenticated GitHub user — id and display name."""

    accounts = "accounts"
    """All accounts visible to the user: the user themselves plus every org they belong to."""

    repos = "repos"
    """All repositories accessible to the user across all accounts."""

    def of(self, username: str) -> str:
        """Return the concrete cache key for a given GitHub username.

        Example::

            >>> CacheKeyEnum.repos.of("alice")
            'repos@alice'
        """
        return f"{self.value}@{username}"
