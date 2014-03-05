#! /usr/bin/env python
# encoding: utf-8
# WARNING! Do not edit! http://waf.googlecode.com/git/docs/wafbook/single.html#_obtaining_the_waf_file

from.import semver
from.import wurf_dependency_bundle
import os
import hashlib
import shutil
from waflib.Logs import debug
git_protocols=['https://','git@','git://']
git_protocol_handler=''
def options(opt):
	git_opts=opt.add_option_group('git options')
	git_opts.add_option('--git-protocol',default='https://',dest='git_protocol',help="Use a specific git protocol to download dependencies. ""Supported protocols: {0}".format(git_protocols))
	git_opts.add_option('--check-git-version',default=True,dest='check_git_version',help="Specifies if the minimum git version is checked")
def configure(conf):
	conf.load('wurf_git')
	if conf.options.check_git_version==True:
		conf.git_check_minimum_version((1,7,0))
	parent_url=None
	try:
		parent_url=conf.git_config(['--get','remote.origin.url'],cwd=os.getcwd())
	except Exception ,e:
		conf.to_log('Exception when executing git config - fallback to ''default protocol! parent_url: {0}'.format(parent_url))
		conf.to_log(e)
	global git_protocol_handler
	if parent_url:
		if parent_url.startswith('https://'):
			git_protocol_handler='https://'
		elif parent_url.startswith('git@'):
			git_protocol_handler='git@'
		elif parent_url.startswith('git://'):
			git_protocol_handler='git://'
		else:
			conf.fatal('Unknown git protocol: {0}'.format(parent_url))
	else:
		git_protocol_handler=conf.options.git_protocol
	if git_protocol_handler not in git_protocols:
		conf.fatal('Unknown git protocol specified: {}, supported protocols ''are {}'.format(git_protocol_handler,git_protocols))
class ResolveGitMajorVersion(object):
	def __init__(self,name,git_repository,major_version):
		self.name=name
		self.git_repository=git_repository
		self.major_version=major_version
	def repository_url(self,ctx):
		repo_url=self.git_repository
		if repo_url.count('://')>0 or repo_url.count('@')>0:
			ctx.fatal('Repository URL contains the following ''git protocol handler: {}'.format(repo_url))
		if git_protocol_handler not in git_protocols:
			ctx.fatal('Unknown git protocol specified: {}, supported protocols ''are {}'.format(git_protocol_handler,git_protocols))
		if git_protocol_handler=='git@':
			if repo_url.startswith('github.com/'):
				repo_url=repo_url.replace('github.com/','github.com:',1)
			else:
				ctx.fatal('Unknown SSH host: {}'.format(repo_url))
		return git_protocol_handler+repo_url
	def resolve(self,ctx,path,use_checkout):
		path=os.path.abspath(os.path.expanduser(path))
		repo_url=self.repository_url(ctx)
		repo_hash=hashlib.sha1(repo_url.encode('utf-8')).hexdigest()[:6]
		repo_folder=os.path.join(path,self.name+'-'+repo_hash)
		if not os.path.exists(repo_folder):
			ctx.to_log("Creating new repository folder: {}".format(repo_folder))
			os.makedirs(repo_folder)
		master_path=os.path.join(repo_folder,'master')
		if not os.path.isdir(master_path):
			ctx.git_clone(repo_url,master_path,cwd=repo_folder)
		try:
			ctx.git_pull(cwd=master_path)
		except Exception ,e:
			ctx.to_log('Exception when executing git pull:')
			ctx.to_log(e)
		if ctx.git_has_submodules(master_path):
			ctx.git_submodule_sync(cwd=master_path)
			ctx.git_submodule_init(cwd=master_path)
			ctx.git_submodule_update(cwd=master_path)
		if use_checkout:
			checkout_path=os.path.join(repo_folder,use_checkout)
			if use_checkout!='master':
				if not os.path.isdir(checkout_path):
					ctx.git_clone(repo_url,checkout_path,cwd=repo_folder)
					ctx.git_checkout(use_checkout,cwd=checkout_path)
				else:
					ctx.git_pull(cwd=checkout_path)
				if ctx.git_has_submodules(checkout_path):
					ctx.git_submodule_sync(cwd=checkout_path)
					ctx.git_submodule_init(cwd=checkout_path)
					ctx.git_submodule_update(cwd=checkout_path)
			tags=ctx.git_tags(cwd=checkout_path)
			for tag in tags:
				try:
					if semver.parse(tag)['major']>self.major_version:
						ctx.fatal('Tag %r in checkout %r is newer than ''the required major version %r'%(tag,use_checkout,self.major_version))
				except ValueError:
					pass
			return checkout_path
		tags=[]
		try:
			tags=ctx.git_tags(cwd=master_path)
		except Exception ,e:
			ctx.to_log('Exception when executing git tags:')
			ctx.to_log(e)
			tags=[d for d in os.listdir(repo_folder)if os.path.isdir(os.path.join(repo_folder,d))]
		if len(tags)==0:
			ctx.fatal('No version tags specified for %r ''- impossible to track major version'%self.name)
		tag=self.select_tag(tags)
		if not tag:
			ctx.fatal('No compatible tags found %r ''to track major version %d of %s'%(tags,self.major_version,self.name))
		tag_path=os.path.join(repo_folder,tag)
		if not os.path.isdir(tag_path):
			ctx.git_local_clone(master_path,tag_path,cwd=repo_folder)
			ctx.git_checkout(tag,cwd=tag_path)
			if ctx.git_has_submodules(tag_path):
				ctx.git_submodule_sync(cwd=tag_path)
				ctx.git_submodule_init(cwd=tag_path)
				ctx.git_submodule_update(cwd=tag_path)
		return tag_path
	def select_tag(self,tags):
		valid_tags=[]
		for t in tags:
			try:
				if semver.parse(t)['major']==self.major_version:
					valid_tags.append(t)
			except ValueError:
				pass
		if len(valid_tags)==0:
			return None
		best_match=valid_tags[0]
		for t in valid_tags:
			if semver.match(best_match,"<"+t):
				best_match=t
		return best_match
	def __eq__(self,other):
		return((self.git_repository.lower(),self.major_version)==(other.git_repository.lower(),other.major_version))
	def __ne__(self,other):
		return not self==other
	def __lt__(self,other):
		return((self.git_repository.lower(),self.major_version)<(other.git_repository.lower(),other.major_version))
	def __repr__(self):
		f='ResolveGitMajorVersion(name=%s, git_repository=%s, major_version=%s)'
		return f%(self.name,self.git_repository,self.major_version)
