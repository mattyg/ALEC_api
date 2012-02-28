from fabric.api import *
from fabric.contrib.console import confirm

env.hosts = ('gabrenya.com')
env.users = ('gabrenya')


def pack():
    local('tar czf /tmp/ALECZombies.tgz .')

def deploy():
    update_source()
    deploy_gabrenya()


def deploy_gabrenya():
    #put('/tmp/ALECZombies.tgz', '/tmp/')
    with cd('/home/gabrenya/www/'):
        #run('tar xzf /tmp/ALECZombies')
        run('/home/gabrenya/opt/bin/python ALECZombies/api.py')

def deploy_source():
    pass
