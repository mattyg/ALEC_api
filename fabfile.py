from fabric.api import *
from fabric.contrib.console import confirm

env.hosts = ('gabrenya@gabrenya.com:22')
env.passwords = {'gabrenya@gabrenya.com:22':'tent29'}

def deploy():
	update_source()
	deploy_gabrenya()

name = 'ALECZombies'
@hosts('gabrenya@gabrenya.com:22')
def deploy_gabrenya():
	local('mv static ../static-backup')
	local('tar czf /tmp/ALEC_api.tgz .')
	local('mv ../static-backup static')
	put('/tmp/ALEC_api.tgz', '/tmp/')
	with cd('/home/gabrenya/www/'):
		run('tar xzf /tmp/ALEC_api')
		run('mv '+name+'/static static-backup')
		run('mv /tmp/ALEC_api .')
		run('mv static-backup ALEC_api/static')
		run('/home/gabrenya/opt/bin/python ALEC_api/api.py')

def update_source():
	local('cp templates/main.md README')
	local('git add -A && git commit && git push origin master')
