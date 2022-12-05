# test_rail_integration_plugin

Environment variables:
Required:
- EXPORT_RESULT_IN_TR - set True for export tests results to Test Rail;
- TEST_RAIL_HOST - url of your Test Rail (e.g. "https://your_testrail.testrail.io");
- TEST_RAIL_TOKEN - your Test Rail api token;
- TEST_RAIL_USERNAME - your Test Rail email;
- RUN_ID_TR - unique run id where results will be exported;

Optional:
- TEST_RAIL_PROJECT - unique id of needed Test Rail project (default: 1);
- TEST_RAIL_COMMENT - comment, what will be added to each exported result;
- TEST_RAIL_VERSION - version, what will be added to each exported result;

How to implement in project:
1. Copy project to your repository;
2. Make changes (if needed);
3. Create release;
4. Change "download_url" in file setup.py (path to created release);
5. Add plugin path to requirements.txt (for example) - git+%%path_to_copied_repository%%:
```commandline
git+https://gitlab2.eleks-software.local/python/test_rail_integration_plugin
```

For any questions, contact **Maksym Biriukov (Maksym.Biriukov@eleks.com)**