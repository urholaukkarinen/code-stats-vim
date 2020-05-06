from codestats import CodeStats


def init_codestats(base_url, api_key):
    """Plugin startup/reload.

    This file should be loaded with pyfile/py3file/pyxfile so it can access
    and modify user namespace globals.

    This function unloads previously running version (if any) and initializes
    the `codestats` global to a running CodeStats instance.
    """
    global codestats

    xp_dict = {}
    # allow reentrancy
    if 'codestats' in globals():
        xp_dict = codestats.xp_dict    # noqa: F821
        del(codestats)

    codestats = CodeStats(xp_dict, base_url, api_key)
