"""Integration tests for all the Python components"""
import sys

# setup mocks
import vim
vim.set_eval({
    's:codestats_path': '',
    'g:codestats_api_key': 'FAKE_API_KEY',
    'g:codestats_api_url': 'http://localhost:8080'
})


def test_codestats_init():
    _run_codestats_py()
    assert('codestats' in globals())
    _stop()


def test_codestats_hot_reload():
    global codestats
    _run_codestats_py()
    codestats.instance = "FIRST INSTANCE"
    _run_codestats_py()
    assert(not hasattr(codestats, 'instance'))
    _stop()


def _run_codestats_py():
    """Run codestats.py like Vim does it, for both Python 2/3"""
    filename = 'plugin/codestats.py'
    scope = sys._getframe(1).f_globals
    if sys.version_info.major == 2:
        execfile(filename, scope, scope)  # noqa F821
    else:
        with open(filename, 'rb') as f:
            code = compile(f.read(), filename, 'exec')
            exec(code, scope, scope)


def _stop():
    """Stop the plugin (because multiprocessing)"""
    global codestats
    del codestats
