from fabric.api import *
from fabric.contrib.console import confirm

env.hosts = ('gabrenya.com')
env.users = ('gabrenya')

def deploy():
	update_source()
	deploy_gabrenya()

name = 'ALECZombies'
def deploy_gabrenya():
	local('mv static ../static-backup')
	local('tar czf /tmp/ALEC_api.tgz .')
	put('/tmp/ALEC_api.tgz', '/tmp/')
	with cd('/home/gabrenya/www/'):
		run('tar xzf /tmp/ALEC_api')
		run('mv '+name+'/static static-backup')
		run('mv /tmp/ALEC_api .')
		run('/home/gabrenya/opt/bin/python ALEC_api/api.py')

def update_source():
	local('git add -A && git commit && git push origin master')
