import os
import asyncio
import functools
import inspect
import json
import sys
from typing import Dict, Any, List, Callable, Coroutine, Union, Optional

from code.approve_final_test_report import approve_final_test_report
from code.compile_backend_code import compile_backend_code
from code.compile_lexer_code import compile_lexer_code
from code.compile_optimizer_code import compile_optimizer_code
from code.compile_parser_code import compile_parser_code
from code.create_backend_directory import create_backend_directory
from code.create_build_directory import create_build_directory
from code.create_developer_guide_directory import create_developer_guide_directory
from code.create_docs_directory import create_docs_directory
from code.create_integration_tests_directory import create_integration_tests_directory
from code.create_lexer_directory import create_lexer_directory
from code.create_optimizer_directory import create_optimizer_directory
from code.create_parser_directory import create_parser_directory
from code.create_src_directory import create_src_directory
from code.create_test_directory import create_test_directory
from code.create_unit_tests_directory import create_unit_tests_directory
from code.create_user_guide_directory import create_user_guide_directory
from code.define_project_root_directory import define_project_root_directory
from code.fix_test_issues import fix_test_issues
from code.generate_final_test_report import generate_final_test_report
from code.generate_integration_test_report import generate_integration_test_report
from code.generate_unit_test_report import generate_unit_test_report
from code.link_backend_with_other_components import link_backend_with_other_components
from code.link_lexer_with_other_components import link_lexer_with_other_components
from code.link_optimizer_with_other_components import link_optimizer_with_other_components
from code.link_parser_with_other_components import link_parser_with_other_components
from code.package_compiler import package_compiler
from code.prepare_for_release import prepare_for_release
from code.publish_compiler import publish_compiler
from code.publish_developer_guide import publish_developer_guide
from code.publish_user_guide import publish_user_guide
from code.re_run_tests import re_run_tests
from code.review_test_reports import review_test_reports
from code.run_integration_tests import run_integration_tests
from code.run_unit_tests import run_unit_tests
from code.write_backend_code import write_backend_code
from code.write_developer_guide import write_developer_guide
from code.write_integration_tests import write_integration_tests
from code.write_lexer_code import write_lexer_code
from code.write_optimizer_code import write_optimizer_code
from code.write_parser_code import write_parser_code
from code.write_unit_tests import write_unit_tests
from code.write_user_guide import write_user_guide

# Get async mode from environment variable or default to False
ASYNC_MODE = os.environ.get('ASYNC_MODE', '').lower() in ('true', '1', 'yes', 'y')

def make_async(func):
    """Convert a synchronous function to an asynchronous function.

    If the function is already asynchronous, return it unchanged.
    If the function is synchronous, wrap it in an async function.
    """
    # If it's already a coroutine function, return it as is
    if inspect.iscoroutinefunction(func):
        return func

    # Otherwise, wrap it as an async function
    @functools.wraps(func)
    async def async_wrapper(*args, **kwargs):
        return func(*args, **kwargs)

    return async_wrapper

approve_final_test_report_async = make_async(approve_final_test_report)
compile_backend_code_async = make_async(compile_backend_code)
compile_lexer_code_async = make_async(compile_lexer_code)
compile_optimizer_code_async = make_async(compile_optimizer_code)
compile_parser_code_async = make_async(compile_parser_code)
create_backend_directory_async = make_async(create_backend_directory)
create_build_directory_async = make_async(create_build_directory)
create_developer_guide_directory_async = make_async(create_developer_guide_directory)
create_docs_directory_async = make_async(create_docs_directory)
create_integration_tests_directory_async = make_async(create_integration_tests_directory)
create_lexer_directory_async = make_async(create_lexer_directory)
create_optimizer_directory_async = make_async(create_optimizer_directory)
create_parser_directory_async = make_async(create_parser_directory)
create_src_directory_async = make_async(create_src_directory)
create_test_directory_async = make_async(create_test_directory)
create_unit_tests_directory_async = make_async(create_unit_tests_directory)
create_user_guide_directory_async = make_async(create_user_guide_directory)
define_project_root_directory_async = make_async(define_project_root_directory)
fix_test_issues_async = make_async(fix_test_issues)
generate_final_test_report_async = make_async(generate_final_test_report)
generate_integration_test_report_async = make_async(generate_integration_test_report)
generate_unit_test_report_async = make_async(generate_unit_test_report)
link_backend_with_other_components_async = make_async(link_backend_with_other_components)
link_lexer_with_other_components_async = make_async(link_lexer_with_other_components)
link_optimizer_with_other_components_async = make_async(link_optimizer_with_other_components)
link_parser_with_other_components_async = make_async(link_parser_with_other_components)
package_compiler_async = make_async(package_compiler)
prepare_for_release_async = make_async(prepare_for_release)
publish_compiler_async = make_async(publish_compiler)
publish_developer_guide_async = make_async(publish_developer_guide)
publish_user_guide_async = make_async(publish_user_guide)
re_run_tests_async = make_async(re_run_tests)
review_test_reports_async = make_async(review_test_reports)
run_integration_tests_async = make_async(run_integration_tests)
run_unit_tests_async = make_async(run_unit_tests)
write_backend_code_async = make_async(write_backend_code)
write_developer_guide_async = make_async(write_developer_guide)
write_integration_tests_async = make_async(write_integration_tests)
write_lexer_code_async = make_async(write_lexer_code)
write_optimizer_code_async = make_async(write_optimizer_code)
write_parser_code_async = make_async(write_parser_code)
write_unit_tests_async = make_async(write_unit_tests)
write_user_guide_async = make_async(write_user_guide)

async def run_workflow(user_input: str) -> Dict[str, Any]:
    """Execute the workflow by running each level in the topological sort.

    Args:
        user_input: The input string for the workflow

    Returns:
        Dict containing all results keyed by node name
    """
    # Store results for each node
    results = {}

    # Level 0: define_project_root_directory
    async def run_define_project_root_directory():
        # Call the async version of define_project_root_directory with results from dependencies
        return await define_project_root_directory_async(user_input)

    # Run level 0 nodes in parallel
    results['define_project_root_directory'] = await run_define_project_root_directory()

    # Level 1: create_build_directory, create_docs_directory, create_test_directory, create_src_directory
    async def run_create_build_directory():
        # Call the async version of create_build_directory with results from dependencies
        return await create_build_directory_async(results['define_project_root_directory'])

    async def run_create_docs_directory():
        # Call the async version of create_docs_directory with results from dependencies
        return await create_docs_directory_async(results['define_project_root_directory'])

    async def run_create_test_directory():
        # Call the async version of create_test_directory with results from dependencies
        return await create_test_directory_async(results['define_project_root_directory'])

    async def run_create_src_directory():
        # Call the async version of create_src_directory with results from dependencies
        return await create_src_directory_async(results['define_project_root_directory'])

    # Run level 1 nodes in parallel
    level_1_results = await asyncio.gather(run_create_build_directory(), run_create_docs_directory(), run_create_test_directory(), run_create_src_directory())
    results['create_build_directory'] = level_1_results[0]
    results['create_docs_directory'] = level_1_results[1]
    results['create_test_directory'] = level_1_results[2]
    results['create_src_directory'] = level_1_results[3]

    # Level 2: create_unit_tests_directory, create_backend_directory, create_developer_guide_directory, create_parser_directory, create_user_guide_directory, create_integration_tests_directory, create_optimizer_directory, create_lexer_directory
    async def run_create_unit_tests_directory():
        # Call the async version of create_unit_tests_directory with results from dependencies
        return await create_unit_tests_directory_async(results['create_test_directory'])

    async def run_create_backend_directory():
        # Call the async version of create_backend_directory with results from dependencies
        return await create_backend_directory_async(results['create_src_directory'])

    async def run_create_developer_guide_directory():
        # Call the async version of create_developer_guide_directory with results from dependencies
        return await create_developer_guide_directory_async(results['create_docs_directory'])

    async def run_create_parser_directory():
        # Call the async version of create_parser_directory with results from dependencies
        return await create_parser_directory_async(results['create_src_directory'])

    async def run_create_user_guide_directory():
        # Call the async version of create_user_guide_directory with results from dependencies
        return await create_user_guide_directory_async(results['create_docs_directory'])

    async def run_create_integration_tests_directory():
        # Call the async version of create_integration_tests_directory with results from dependencies
        return await create_integration_tests_directory_async(results['create_test_directory'])

    async def run_create_optimizer_directory():
        # Call the async version of create_optimizer_directory with results from dependencies
        return await create_optimizer_directory_async(results['create_src_directory'])

    async def run_create_lexer_directory():
        # Call the async version of create_lexer_directory with results from dependencies
        return await create_lexer_directory_async(results['create_src_directory'])

    # Run level 2 nodes in parallel
    level_2_results = await asyncio.gather(run_create_unit_tests_directory(), run_create_backend_directory(), run_create_developer_guide_directory(), run_create_parser_directory(), run_create_user_guide_directory(), run_create_integration_tests_directory(), run_create_optimizer_directory(), run_create_lexer_directory())
    results['create_unit_tests_directory'] = level_2_results[0]
    results['create_backend_directory'] = level_2_results[1]
    results['create_developer_guide_directory'] = level_2_results[2]
    results['create_parser_directory'] = level_2_results[3]
    results['create_user_guide_directory'] = level_2_results[4]
    results['create_integration_tests_directory'] = level_2_results[5]
    results['create_optimizer_directory'] = level_2_results[6]
    results['create_lexer_directory'] = level_2_results[7]

    # Level 3: write_parser_code, write_optimizer_code, write_backend_code, write_lexer_code, write_developer_guide, write_user_guide, write_integration_tests, write_unit_tests
    async def run_write_parser_code():
        # Call the async version of write_parser_code with results from dependencies
        return await write_parser_code_async(results['create_parser_directory'])

    async def run_write_optimizer_code():
        # Call the async version of write_optimizer_code with results from dependencies
        return await write_optimizer_code_async(results['create_optimizer_directory'])

    async def run_write_backend_code():
        # Call the async version of write_backend_code with results from dependencies
        return await write_backend_code_async(results['create_backend_directory'])

    async def run_write_lexer_code():
        # Call the async version of write_lexer_code with results from dependencies
        return await write_lexer_code_async(results['create_lexer_directory'])

    async def run_write_developer_guide():
        # Call the async version of write_developer_guide with results from dependencies
        return await write_developer_guide_async(results['create_developer_guide_directory'])

    async def run_write_user_guide():
        # Call the async version of write_user_guide with results from dependencies
        return await write_user_guide_async(results['create_user_guide_directory'])

    async def run_write_integration_tests():
        # Call the async version of write_integration_tests with results from dependencies
        return await write_integration_tests_async(results['create_integration_tests_directory'])

    async def run_write_unit_tests():
        # Call the async version of write_unit_tests with results from dependencies
        return await write_unit_tests_async(results['create_unit_tests_directory'])

    # Run level 3 nodes in parallel
    level_3_results = await asyncio.gather(run_write_parser_code(), run_write_optimizer_code(), run_write_backend_code(), run_write_lexer_code(), run_write_developer_guide(), run_write_user_guide(), run_write_integration_tests(), run_write_unit_tests())
    results['write_parser_code'] = level_3_results[0]
    results['write_optimizer_code'] = level_3_results[1]
    results['write_backend_code'] = level_3_results[2]
    results['write_lexer_code'] = level_3_results[3]
    results['write_developer_guide'] = level_3_results[4]
    results['write_user_guide'] = level_3_results[5]
    results['write_integration_tests'] = level_3_results[6]
    results['write_unit_tests'] = level_3_results[7]

    # Level 4: publish_user_guide, run_unit_tests, publish_developer_guide, run_integration_tests, compile_parser_code, compile_lexer_code, compile_optimizer_code, compile_backend_code
    async def run_publish_user_guide():
        # Call the async version of publish_user_guide with results from dependencies
        return await publish_user_guide_async(results['write_user_guide'])

    async def run_run_unit_tests():
        # Call the async version of run_unit_tests with results from dependencies
        return await run_unit_tests_async(results['write_unit_tests'])

    async def run_publish_developer_guide():
        # Call the async version of publish_developer_guide with results from dependencies
        return await publish_developer_guide_async(results['write_developer_guide'])

    async def run_run_integration_tests():
        # Call the async version of run_integration_tests with results from dependencies
        return await run_integration_tests_async(results['write_integration_tests'])

    async def run_compile_parser_code():
        # Call the async version of compile_parser_code with results from dependencies
        return await compile_parser_code_async(results['write_parser_code'])

    async def run_compile_lexer_code():
        # Call the async version of compile_lexer_code with results from dependencies
        return await compile_lexer_code_async(results['write_lexer_code'])

    async def run_compile_optimizer_code():
        # Call the async version of compile_optimizer_code with results from dependencies
        return await compile_optimizer_code_async(results['write_optimizer_code'])

    async def run_compile_backend_code():
        # Call the async version of compile_backend_code with results from dependencies
        return await compile_backend_code_async(results['write_backend_code'])

    # Run level 4 nodes in parallel
    level_4_results = await asyncio.gather(run_publish_user_guide(), run_run_unit_tests(), run_publish_developer_guide(), run_run_integration_tests(), run_compile_parser_code(), run_compile_lexer_code(), run_compile_optimizer_code(), run_compile_backend_code())
    results['publish_user_guide'] = level_4_results[0]
    results['run_unit_tests'] = level_4_results[1]
    results['publish_developer_guide'] = level_4_results[2]
    results['run_integration_tests'] = level_4_results[3]
    results['compile_parser_code'] = level_4_results[4]
    results['compile_lexer_code'] = level_4_results[5]
    results['compile_optimizer_code'] = level_4_results[6]
    results['compile_backend_code'] = level_4_results[7]

    # Level 5: generate_integration_test_report, link_lexer_with_other_components, link_optimizer_with_other_components, link_parser_with_other_components, link_backend_with_other_components, generate_unit_test_report
    async def run_generate_integration_test_report():
        # Call the async version of generate_integration_test_report with results from dependencies
        return await generate_integration_test_report_async(results['run_integration_tests'])

    async def run_link_lexer_with_other_components():
        # Call the async version of link_lexer_with_other_components with results from dependencies
        return await link_lexer_with_other_components_async(results['compile_parser_code'], results['compile_lexer_code'], results['compile_optimizer_code'], results['compile_backend_code'])

    async def run_link_optimizer_with_other_components():
        # Call the async version of link_optimizer_with_other_components with results from dependencies
        return await link_optimizer_with_other_components_async(results['compile_parser_code'], results['compile_lexer_code'], results['compile_optimizer_code'], results['compile_backend_code'])

    async def run_link_parser_with_other_components():
        # Call the async version of link_parser_with_other_components with results from dependencies
        return await link_parser_with_other_components_async(results['compile_parser_code'], results['compile_lexer_code'], results['compile_optimizer_code'], results['compile_backend_code'])

    async def run_link_backend_with_other_components():
        # Call the async version of link_backend_with_other_components with results from dependencies
        return await link_backend_with_other_components_async(results['compile_parser_code'], results['compile_lexer_code'], results['compile_optimizer_code'], results['compile_backend_code'])

    async def run_generate_unit_test_report():
        # Call the async version of generate_unit_test_report with results from dependencies
        return await generate_unit_test_report_async(results['run_unit_tests'])

    # Run level 5 nodes in parallel
    level_5_results = await asyncio.gather(run_generate_integration_test_report(), run_link_lexer_with_other_components(), run_link_optimizer_with_other_components(), run_link_parser_with_other_components(), run_link_backend_with_other_components(), run_generate_unit_test_report())
    results['generate_integration_test_report'] = level_5_results[0]
    results['link_lexer_with_other_components'] = level_5_results[1]
    results['link_optimizer_with_other_components'] = level_5_results[2]
    results['link_parser_with_other_components'] = level_5_results[3]
    results['link_backend_with_other_components'] = level_5_results[4]
    results['generate_unit_test_report'] = level_5_results[5]

    # Level 6: review_test_reports
    async def run_review_test_reports():
        # Call the async version of review_test_reports with results from dependencies
        return await review_test_reports_async(results['generate_unit_test_report'], results['generate_integration_test_report'])

    # Run level 6 nodes in parallel
    results['review_test_reports'] = await run_review_test_reports()

    # Level 7: fix_test_issues
    async def run_fix_test_issues():
        # Call the async version of fix_test_issues with results from dependencies
        return await fix_test_issues_async(results['review_test_reports'])

    # Run level 7 nodes in parallel
    results['fix_test_issues'] = await run_fix_test_issues()

    # Level 8: re_run_tests
    async def run_re_run_tests():
        # Call the async version of re_run_tests with results from dependencies
        return await re_run_tests_async(results['fix_test_issues'])

    # Run level 8 nodes in parallel
    results['re_run_tests'] = await run_re_run_tests()

    # Level 9: generate_final_test_report
    async def run_generate_final_test_report():
        # Call the async version of generate_final_test_report with results from dependencies
        return await generate_final_test_report_async(results['re_run_tests'])

    # Run level 9 nodes in parallel
    results['generate_final_test_report'] = await run_generate_final_test_report()

    # Level 10: approve_final_test_report
    async def run_approve_final_test_report():
        # Call the async version of approve_final_test_report with results from dependencies
        return await approve_final_test_report_async(results['generate_final_test_report'])

    # Run level 10 nodes in parallel
    results['approve_final_test_report'] = await run_approve_final_test_report()

    # Level 11: prepare_for_release
    async def run_prepare_for_release():
        # Call the async version of prepare_for_release with results from dependencies
        return await prepare_for_release_async(results['approve_final_test_report'])

    # Run level 11 nodes in parallel
    results['prepare_for_release'] = await run_prepare_for_release()

    # Level 12: package_compiler
    async def run_package_compiler():
        # Call the async version of package_compiler with results from dependencies
        return await package_compiler_async(results['prepare_for_release'])

    # Run level 12 nodes in parallel
    results['package_compiler'] = await run_package_compiler()

    # Level 13: publish_compiler
    async def run_publish_compiler():
        # Call the async version of publish_compiler with results from dependencies
        return await publish_compiler_async(results['package_compiler'])

    # Run level 13 nodes in parallel
    results['publish_compiler'] = await run_publish_compiler()

    # Return all results
    return results

def run_workflow_sync(user_input: str) -> Dict[str, Any]:
    """Synchronous wrapper around the async workflow execution."""
    return asyncio.run(run_workflow(user_input))

def main():
    """Main entry point.

    Handles arguments in the following priority:
    1. Command-line argument (sys.argv[1])
    2. If no argument, uses empty string as input but displays a warning.
    """
    # Get user input from command line or use empty string
    if len(sys.argv) > 1:
        user_input = sys.argv[1]
    else:
        # No input provided - display help message but continue with empty string
        print('Warning: No input provided. Using empty string as input.')
        print('For better results, provide an input argument:')
        print(f'  python {os.path.basename(__file__)} "your input text here"')
        print('Or use a file as input:')
        print(f'  python {os.path.basename(__file__)} "$(cat input.txt)"')
        user_input = ""

    print(f'Running workflow with input: {user_input}')

    # Run the workflow
    results = run_workflow_sync(user_input)

    # Print results
    try:
        # Convert results to JSON
        json_results = json.dumps(results, indent=2, default=str)
        print(json_results)
    except (TypeError, ValueError) as e:
        print(f'Results could not be converted to JSON: {e}')
        print(f'Raw results: {results}')

    return results

if __name__ == '__main__':
    main()
