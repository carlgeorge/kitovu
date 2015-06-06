import os
import pathlib


def get_xdg_path(variable):
    try:
        return pathlib.Path(os.environ[variable])
    except KeyError:
        try:
            home = pathlib.Path(os.environ['HOME'])
        except KeyError:
            raise SystemExit('HOME not set')
        defaults = {'XDG_CACHE_HOME': home / '.cache',
                    'XDG_CONFIG_HOME': home / '.config',
                    'XDG_DATA_HOME': home / '.local' / 'share',
                    'XDG_STATE_HOME': home / '.local' / 'state'}
        try:
            return defaults[variable]
        except KeyError:
            raise SystemExit('no default stored for ' + variable)


cache_home = get_xdg_path('XDG_CACHE_HOME')
config_home = get_xdg_path('XDG_CONFIG_HOME')
data_home = get_xdg_path('XDG_DATA_HOME')
state_home = get_xdg_path('XDG_STATE_HOME')


def get_resource_path(base, *resource):
    resource = pathlib.Path(*resource)
    assert not resource.is_absolute()
    path = base / resource
    if not path.is_dir():
        path.mkdir(parents=True)
    return path


def get_cache_path(*resource):
    return get_resource_path(cache_home, *resource)


def get_config_path(*resource):
    return get_resource_path(config_home, *resource)


def get_data_path(*resource):
    return get_resource_path(data_home, *resource)


def get_state_path(*resource):
    return get_resource_path(state_home, *resource)
