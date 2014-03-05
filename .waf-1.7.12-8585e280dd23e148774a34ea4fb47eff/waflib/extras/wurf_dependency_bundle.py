#! /usr/bin/env python
# encoding: utf-8
# WARNING! Do not edit! http://waf.googlecode.com/git/docs/wafbook/single.html#_obtaining_the_waf_file

from waflib.Configure import conf
from waflib.Configure import ConfigurationContext
from waflib.Options import OptionsContext
from waflib.ConfigSet import ConfigSet
import waflib.Options as Opt
from waflib import Logs
from waflib import Options
from waflib import Utils
from waflib import Scripting
from waflib import Context
from waflib import Errors
import sys
import os
import shutil
OPTIONS_NAME='dependency options'
DEFAULT_BUNDLE='ALL'
DEFAULT_BUNDLE_PATH='bundle_dependencies'
DEPENDENCY_PATH_KEY='%s_DEPENDENCY_PATH'
DEPENDENCY_CHECKOUT_KEY='%s_DEPENDENCY_CHECKOUT'
dependencies=dict()
def add_dependency(opt,resolver):
	name=resolver.name
	if name in dependencies:
		if type(resolver)!=type(dependencies[name])or dependencies[name]!=resolver:
			raise Errors.WafError('Incompatible dependency added %r <=> %r '%(resolver,dependencies[name]))
	else:
		dependencies[name]=resolver
def expand_path(path):
	return os.path.abspath(os.path.expanduser(path))
def options(opt):
	opt.load('wurf_dependency_resolve')
	bundle_opts=opt.add_option_group(OPTIONS_NAME)
	add=bundle_opts.add_option
	add('--bundle',default=DEFAULT_BUNDLE,dest='bundle',help="Which dependencies to bundle")
	add('--bundle-path',default=DEFAULT_BUNDLE_PATH,dest='bundle_path',help="The folder used for downloaded dependencies")
	for dependency in dependencies:
		add('--%s-path'%dependency,dest=DEPENDENCY_PATH_KEY%dependency,default=False,help='path to %s'%dependency)
		add('--%s-use-checkout'%dependency,dest=DEPENDENCY_CHECKOUT_KEY%dependency,default=False,help='The checkout to use for %s'%dependency)
def configure(conf):
	conf.load('wurf_dependency_resolve')
	bundle_path=expand_path(conf.options.bundle_path)
	bundle_list=expand_bundle(conf,conf.options.bundle)
	explicit_list=explicit_dependencies(conf.options)
	overlap=set(bundle_list).intersection(set(explicit_list))
	if len(overlap)>0:
		conf.fatal("Overlapping dependencies %r"%overlap)
	conf.env['BUNDLE_DEPENDENCIES']=dict()
	for name in bundle_list:
		Utils.check_dir(bundle_path)
		conf.start_msg('Resolve dependency %s'%name)
		key=DEPENDENCY_CHECKOUT_KEY%name
		dependency_checkout=getattr(conf.options,key,None)
		dependency_path=dependencies[name].resolve(ctx=conf,path=bundle_path,use_checkout=dependency_checkout)
		conf.end_msg(dependency_path)
		conf.env['BUNDLE_DEPENDENCIES'][name]=dependency_path
	for name in explicit_list:
		key=DEPENDENCY_PATH_KEY%name
		dependency_path=getattr(conf.options,key)
		dependency_path=expand_path(dependency_path)
		conf.start_msg('User resolve dependency %s'%name)
		conf.env['BUNDLE_DEPENDENCIES'][name]=dependency_path
		conf.end_msg(dependency_path)
def expand_bundle(conf,arg):
	if not arg:
		return[]
	arg=arg.split(',')
	if'NONE'in arg and'ALL'in arg:
		conf.fatal('Cannot specify both ALL and NONE as dependencies')
	candidate_score=dict([(name,0)for name in dependencies])
	def check_candidate(c):
		if c not in candidate_score:
			conf.fatal('Cannot bundle %s, since it is not specified as a'' dependency'%c)
	for a in arg:
		if a=='ALL':
			for candidate in candidate_score:
				candidate_score[candidate]+=1
			continue
		if a=='NONE':
			continue
		if a.startswith('-'):
			a=a[1:]
			check_candidate(a)
			candidate_score[a]-=1
		else:
			check_candidate(a)
			candidate_score[a]+=1
	candidates=[name for name in candidate_score if candidate_score[name]>0]
	return candidates
def explicit_dependencies(options):
	explicit_list=[]
	for name in dependencies:
		key=DEPENDENCY_PATH_KEY%name
		path=getattr(options,key,None)
		if path:explicit_list.append(name)
	return explicit_list
@conf
def has_dependency_path(self,name):
	if name in self.env['BUNDLE_DEPENDENCIES']:
		return True
	return False
@conf
def dependency_path(self,name):
	return self.env['BUNDLE_DEPENDENCIES'][name]
@conf
def is_toplevel(self):
	return self.srcnode==self.path
