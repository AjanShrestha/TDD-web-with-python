from fabric.contrib.files import append, exists, sed
from fabric.api import env, local, run
import random
import string

REPO_URL = 'https://github.com/AjanShrestha/TDD-web-with-python.git'


def deploy():
    site_folder = f'/home/{env.user}/sites/{env.host}'
    source_folder = site_folder + '/source'
    _create_directory_structure_if_necessary(site_folder)
    _get_latest_source(source_folder)
    _update_settings(source_folder, env.host)
    _update_virtualenv(source_folder)
    _update_static_files(source_folder)
    _update_database(source_folder)


def _create_directory_structure_if_necessary(site_folder):
    for subfolder in ('database', 'static', 'virtualenv', 'source'):
        run(f'mkdir -p {site_folder}/{subfolder}')


def _get_latest_source(source_folder):
    if exists(source_folder + '/.git'):
        run(f'cd {source_folder} && git fetch')
    else:
        run(f'git clone {REPO_URL} {source_folder}')
    current_commit = local("git log -n 1 --format=%H", capture=True)
    # Fabric’s local command runs a command on your local
    # machine—it’s just a wrapper around subprocess.Popen really, but
    # it’s quite convenient. Here we capture the output from that git
    # log invocation to get the ID of the current commit that’s on
    # your local PC. That means the server will end up with whatever
    # code is currently checked out on your machine (as long as
    # you’ve pushed it up to the server).
    run(f'cd {source_folder} && git reset --hard {current_commit}')
    # We reset --hard to that commit, which will blow away any
    # current changes in the server’s code directory.

    # The end result of this is that we either do a git clone if it’s
    # a fresh deploy, or we do a git fetch + git reset --hard if a
    # previous version of the code is already there; the equivalent
    # of the git pull we used when we did it manually, but with the
    # reset -- hard to force overwriting any local changes.


def _update_settings(source_folder, site_name):
    settings_path = source_folder + '/superlists/settings.py'
    sed(settings_path, "DEBUG = True", "DEBUG = False")
    sed(settings_path,
        'ALLOWED_HOSTS =.+$',
        f'ALLOWED_HOSTS = ["{site_name}"]'
        )
    secret_key_file = source_folder + '/superlists/secret_key.py'
    # Django uses SECRET_KEY for some of its crypto—things like
    # cookies and CSRF protection. It’s good practice to make sure
    # the secret key on the server is different from the one in your
    # source code repo, because that code might be visible to
    # strangers. This section will generate a new key to import into
    # settings, if there isn’t one there already (once you have a
    # secret key, it should stay the same between deploys).
    if not exists(secret_key_file):
        chars = string.ascii_lowercase + string.digits + '!@#$%^&*(-_=+)'
        key = ''.join(random.SystemRandom().choice(chars) for _ in range(50))
        append(secret_key_file, f'SECRET_KEY = {key}')
    append(settings_path, '\nfrom .secret_key import SECRET_KEY')
    # append just adds a line to the end of a file. (It’s clever
    # enough not to bother if the line is already there, but not
    # clever enough to automatically add a newline if the file
    # doesn’t end in one. Hence the back-n.)
    # I’m using a relative import (from .secret_key instead of from
    # secret_key) to be absolutely sure we’re importing the local
    # module, rather than one from some‐ where else on sys.path.


def _update_virtualenv(source_folder):
    virtualenv_folder = source_folder + '/../virtualenv'
    if not exists(virtualenv_folder + '/bin/pip'):
        run(f'python3 -m venv {virtualenv_folder}')
    run(f'{virtualenv_folder}/bin/pip install -r {source_folder}/requirements.txt')


def _update_static_files(source_folder):
    run(
        f'cd {source_folder}'
        ' && ../virtualenv/bin/python manage.py collectstatic --noinput'
    )


def _update_database(source_folder):
    run(
        f'cd {source_folder}'
        ' && ../virtualenv/bin/python manage.py migrate --noinput'
    )
    # The --noinput removes any interactive yes/no confirmations that
    # Fabric would find hard to deal with.


#                        Fabric Configuration
# If you are using an SSH key to log in, are storing it in the
# default location, and are using the same username on the server as
# locally, then Fabric should “just work”. If you aren’t, there are
# several tweaks you may need to apply in order to get the fab
# command to do your bidding. They revolve around the username, the
# location of the SSH key to use, or the password.

# You can pass these in to Fabric at the command line. Check out:
#       $ fab --help
# Or see the Fabric documentation for more info.
