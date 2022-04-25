# -*- coding: utf-8 -*-

from pathlib_mate import Path

dir_home = Path.home()

dir_alfred_workflow = Path(dir_home, ".alfred-afwf_github")
dir_cache = Path(dir_alfred_workflow, ".cache")
path_default_token = Path(dir_alfred_workflow, "default")
dir_org_index = Path(dir_alfred_workflow, "org_index")
dir_repo_index = Path(dir_alfred_workflow, "repo_index")

dir_here = Path.dir_here(__file__)
dir_project_root = dir_here.parent
dir_cache_for_test = Path(dir_project_root, "tests", ".cache")
dir_org_index_for_test = Path(dir_project_root, "tests", "org_index")
dir_repo_index_for_test = Path(dir_project_root, "tests", "repo_index")
path_org_json = Path(dir_here, "tests", "orgs.json")
path_repo_json = Path(dir_here, "tests", "repos.json")
