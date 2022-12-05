import re
from typing import List

import pytest
from _pytest.python import Function
from _pytest.reports import TestReport

from test_rail.rail_client import TestRail
from test_rail.service.helpers import get_env
from test_rail.service.test_rail_errors import TestRailError


def pytest_configure():
    if get_env('EXPORT_RESULT_IN_TR') is True:
        run_id = get_env('RUN_ID_TR')
        if run_id is not None:
            test_rail = TestRail(
                host=get_env('TEST_RAIL_HOST'),
                token=get_env('TEST_RAIL_TOKEN'),
                username=get_env('TEST_RAIL_USERNAME'),
                default_project_id=get_env('TEST_RAIL_PROJECT', 1))
            if test_rail.runs.is_have_run(run_id):

                # Setting created TestRail Client to pytest
                setattr(pytest, 'test_rail', test_rail)

                # Setting array for results to pytest
                setattr(pytest, 'test_rail_results', [])

                # Setting array for error to pytest
                setattr(pytest, 'test_rail_errors', [])

                # Setting tests from TestRail
                setattr(pytest, 'tr_tests', test_rail.api_tests.get_tests(
                    run_id))

                # Setting comment text
                setattr(pytest, 'tr_comment', get_env('TEST_RAIL_COMMENT'))

            else:
                raise TestRailError(
                    f"Can't find run with id {run_id}")
        else:
            raise TestRailError(
                'EXPORT_RESULT_IN_TR is True, but RUN_ID_TR is None')


def pytest_runtest_teardown(item: Function):
    if hasattr(pytest, 'test_rail'):
        # adding test result to results array after each test
        test_ids = get_test_id(item)
        if test_ids is None:
            pytest.test_rail_errors.append(item.nodeid)
            return

        rep_setup: TestReport = item.rep_setup
        comment = ''
        if rep_setup.skipped is True:
            default_skip_text = 'Test was skipped'
            status_id = pytest.test_rail.skip_status
            if isinstance(rep_setup.longrepr, tuple):
                comment = rep_setup.longrepr[-1].split(': ')[-1]
                if 'depends on' in comment:
                    status_id = pytest.test_rail.blocked_status
                    module_tests = get_all_tests_in_module(item)
                    links = []
                    for depends in get_test_depends(item):
                        parent_test = get_test_by_dependency_name(
                            depends, module_tests)
                        if parent_test is None:
                            continue
                        parent_id = get_test_id(parent_test)
                        if parent_id is not None:
                            links.append(
                                f'{pytest.test_rail.case_url}{parent_id}')
                    comment = 'Blocked by:\n' + '\n'.join(links)

                if comment == 'unconditional skip':
                    comment = default_skip_text
            else:
                comment = default_skip_text
            if status_id is None:
                status_id = pytest.test_rail.blocked_status
        else:
            # using different TestReport (in case when test failed on
            #                           startup fixture
            report = item.rep_call if hasattr(item, 'rep_call') else rep_setup
            status_id = pytest.test_rail.fail_status if report.failed \
                else pytest.test_rail.pass_status

        test_result = {
            'case_id': test_ids,
            'status_id': status_id,
            'comment': f'{pytest.tr_comment}\n{comment}'
        }
        pytest.test_rail_results.append(test_result)


def pytest_sessionfinish():
    if hasattr(pytest, 'test_rail'):
        run_id = get_env('RUN_ID_TR')
        test_rail: TestRail = pytest.test_rail
        test_results = pytest.test_rail_results
        tests = pytest.tr_tests
        relations = {test['case_id']: index for index, test in enumerate(tests)}
        missing_cases = [case['case_id'] for case in test_results
                         if case['case_id'] not in relations]
        executed_tests = []

        if len(missing_cases) > 0:
            # Increasing run's cases when some tests doesn't included in run
            cases_ids = missing_cases + [test['case_id'] for test in tests]
            test_rail.runs.update_run(run_id, case_ids=cases_ids)
            tests = test_rail.api_tests.get_tests(run_id)

        export_results, missing_cases = [], []
        for result in test_results:
            executed_tests.append(result['case_id'])
            test_id = next((test['id'] for test in tests
                            if test['case_id'] == result['case_id']), None)
            if test_id is None:
                missing_cases.append(result)
            else:
                obj = {
                    'test_id': test_id,
                    'status_id': result['status_id'],
                    'comment': result['comment'],
                    'version': get_env('TEST_RAIL_VERSION', None)
                }
                export_results.append(obj)
        skipped_tests = tuple(test for test in tests
                              if test['case_id'] not in executed_tests)
        for skip_test in skipped_tests:
            # Marking tests what doesn't included in tests execution,
            # but available in run as skipped
            obj = {
                'test_id': skip_test['id'],
                'status_id': test_rail.skip_status,
                'version': get_env('TEST_RAIL_VERSION', None)
            }
            export_results.append(obj)
        test_rail.results.add_results(
            run_id=run_id, results=export_results)


def get_test_id(item: Function) -> int or None:
    """
    Function for getting test id from test
    :param item: pytest test
    :return: test id (if found) or None
    """
    if hasattr(item, 'callspec'):
        if 'ufapi_dataset' in item.callspec.id:
            test_id = re.findall(r'C(\d+)', item.function.__doc__)
            index = item.callspec.indices['ufapi_dataset']
            if len(test_id) >= index:
                return int(test_id[index])
        elif 'algorithms_evaluation/test_evaluation.py' in item.nodeid:
            test_id = re.findall(r'\d{3,}', item.callspec.id)
            index = 0 if 'model' in item.callspec.id.lower() else 1
            if len(test_id) >= index:
                return int(test_id[index])
        test_id = re.findall(r'\d{3,}',
                             item.callspec.id)
        if len(test_id) == 1:
            return int(test_id[0])
    if item.function.__doc__ is not None:
        test_id = re.findall(r'C(\d{3,})', item.function.__doc__)
        if len(test_id) == 1:
            return int(test_id[0])


def get_all_tests_in_module(item: Function) -> List[Function]:
    return [sub_item for sub_item in item.session.items
            if sub_item.module == item.module]


def get_test_by_dependency_name(dependency_name: str,
                                items: List[Function]) -> Function:
    for item in items:
        if next((mark for mark in item.own_markers
                 if mark.name == 'dependency'
                    and mark.kwargs.get('name') == dependency_name), None):
            return item


def get_test_depends(item: Function) -> List[str]:
    return next((mark.kwargs.get('depends') for mark in item.own_markers
                 if mark.kwargs.get('depends')), None)


def pytest_collection_finish(session):
    """Service function for collecting tests than doesn't have id"""
    all_ids = []
    for item in session.items:
        if get_test_id(item) is None:
            all_ids.append(item)
