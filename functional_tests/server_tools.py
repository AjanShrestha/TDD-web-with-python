from fabric.api import run
from fabric.context_managers import settings


def _get_manage_dot_py(host):
    return f'~/sites/{host}/virtualenv/bin/python ~/sites/{host}/source/manage.py'


def reset_database(host):
    manage_dot_py = _get_manage_dot_py(host)
    with settings(host_string=f'aj@{host}'):  # 1
        run(f'{manage_dot_py} flush --noinput')  # 2


def create_session_on_server(host, email):
    manage_dot_py = _get_manage_dot_py(host)
    with settings(host_string=f'aj@{host}'):  # 1
        session_key = run(f'{manage_dot_py} create_cession {email}')  # 2
        return session_key

# 1. Here’s the context manager that sets the host string, in the
#   form user@server- address
# 2. Then, once we’re inside the context manager, we can just call
#   Fabric commands as if we’re in a fabfile.
