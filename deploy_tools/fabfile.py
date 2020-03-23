from fabric.contrib.files import append, exists, sed
from fabric.api import env, local, run
import random

REPO_URL = 'https://github.com:AjanShrestha/TDD-web-with-python.git'


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
