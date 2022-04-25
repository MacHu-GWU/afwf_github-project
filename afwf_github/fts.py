# -*- coding: utf-8 -*-

"""
Full text search helpers
"""

import shutil
from typing import List

from pathlib_mate import Path
from diskcache import Cache
from whoosh.index import open_dir, create_in, exists_in, FileIndex
from whoosh.fields import SchemaClass, TEXT, KEYWORD, NGRAM, STORED
from whoosh.query import And, Or, Term, MultiTerm
from whoosh.qparser import MultifieldParser

from .paths import dir_org_index, dir_repo_index
from .gh import get_accounts, get_repos
from .cache import cache


def get_index(
    path: Path,
    schema: SchemaClass,
    reset=True,
) -> FileIndex:
    if reset:
        try:
            shutil.rmtree(path.abspath)
        except:
            pass
    path.mkdir_if_not_exists()
    if exists_in(path.abspath):
        return open_dir(path.abspath)
    else:
        return create_in(dirname=path.abspath, schema=schema)


class OrganizationSchema(SchemaClass):
    id = STORED()
    name = STORED()
    id_keyword = KEYWORD(lowercase=True)
    id_ngram = NGRAM(minsize=2, maxsize=10)
    name_keyword = KEYWORD(lowercase=True)
    name_ngram = NGRAM(minsize=2, maxsize=10)


class RepoSchema(SchemaClass):
    acc = STORED()
    repo = STORED()
    desc = STORED()
    repo_name_keyword = KEYWORD(lowercase=True)
    repo_name_ngram = NGRAM(minsize=2, maxsize=10)
    fullname_ngram = NGRAM(minsize=2, maxsize=10)


org_schema = OrganizationSchema()
repo_schema = RepoSchema()


def rebuild_org_index(
    dir_index: Path = dir_org_index,
    cache: Cache = cache,
):
    index = get_index(dir_index, org_schema, reset=True)
    accounts = get_accounts(cache)
    with index.writer(limitmb=128) as writer:
        for account in accounts:
            account_id = account["id"]
            account_name = account["name"]
            writer.add_document(
                id=account_id,
                name=account_name,
                id_keyword=account_id,
                id_ngram=account_id,
                name_keyword=account_name,
                name_ngram=account_name,
            )


def rebuild_repo_index(
    dir_index: Path = dir_repo_index,
    cache: Cache = cache,
):
    index = get_index(dir_index, repo_schema, reset=True)
    repos = get_repos(cache)
    with index.writer(limitmb=128) as writer:
        for repo in repos:
            account_name = repo["acc"]
            repo_name = repo["repo"]
            repo_description = repo.get("desc")
            doc = dict(
                acc=account_name,
                repo=repo_name,
                desc=repo_description,
                repo_name_keyword=repo_name,
                repo_name_ngram=repo_name,
                fullname_ngram=f"{account_name}/{repo_name}",
            )
            writer.add_document(**doc)


def search_org(
    q: str,
    dir_index: Path = dir_org_index,
) -> List[dict]:
    index = get_index(dir_index, org_schema, reset=False)
    docs = list()
    with index.searcher() as sr:
        query = MultifieldParser(
            [
                "id_keyword", "id_ngram",
                "name_keyword", "name_ngram",
            ],
            schema=org_schema,
        ).parse(q)
        results = sr.search(query, limit=20)
        for hit in results:
            doc = hit.fields()
            docs.append(doc)
    return docs


def search_repo(
    q: str,
    dir_index: Path = dir_repo_index,
) -> List[dict]:
    index = get_index(dir_index, repo_schema, reset=False)
    docs = list()
    with index.searcher() as sr:
        query = MultifieldParser(
            ["repo_name_keyword", "repo_name_ngram", "fullname_ngram"],
            schema=repo_schema,
        ).parse(q)
        results = sr.search(query, limit=20)
        for hit in results:
            doc = hit.fields()
            docs.append(doc)
    return docs
