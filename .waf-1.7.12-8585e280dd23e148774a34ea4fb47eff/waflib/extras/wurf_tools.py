#! /usr/bin/env python
# encoding: utf-8
# WARNING! Do not edit! http://waf.googlecode.com/git/docs/wafbook/single.html#_obtaining_the_waf_file

import os,sys
from waflib.Configure import conf
from waflib import Options
def _check_minimum_python_version(opt,major,minor):
	if sys.version_info[:2]<(major,minor):
		opt.fatal("Python version not supported: {0}, ""required minimum version: {1}.{2}".format(sys.version_info[:3],major,minor))
def options(opt):
	_check_minimum_python_version(opt,2,7)
	tool_opts=opt.add_option_group('external tool options')
	tool_opts.add_option('--options',default=None,action="append",dest='tool_options',help="Some external Waf tools requires additional options, you can ""use this option multiple times.")
def parse_options(options_string):
	result={}
	if options_string:
		for options in options_string:
			for option in options.split(','):
				try:
					key,value=option.split('=',1)
					result[key]=value
				except ValueError ,e:
					result[option]=True
	return result
def _read_tool_options(conf):
	conf.env["tool_options"]=parse_options(Options.options.tool_options)
def configure(conf):
	_read_tool_options(conf)
def check_for_duplicate(conf):
	tool_options=Options.options.tool_options
	options=parse_options(tool_options)
	for option in options:
		if(option in conf.env['tool_options']and conf.env['tool_options'][option]!=options[option]):
			conf.fatal("Redefined option '%s' from %s to '%s', ""re-run configure, to override the old value."%(option,conf.env['tool_options'][option],options[option]))
@conf
def get_tool_option(conf,option):
	check_for_duplicate(conf)
	stored=conf.env.tool_options
	passed=parse_options(Options.options.tool_options)
	if option in stored:
		return stored[option]
	elif option in passed:
		return passed[option]
	else:
		conf.fatal('Tool option required %s, you can specify tool options as: ''./waf configure --options=KEY=VALUE,KEY=VALUE'%option)
@conf
def has_tool_option(conf,option):
	check_for_duplicate(conf)
	return(option in conf.env.tool_options or option in parse_options(Options.options.tool_options))
load_error="""
Could not find the external waf-tools. Common reasons
for this are:
   1) The external tools repository was not added as
      a dependency. This is done using the wurf_dependency_bundle
      tool.
   2) The external tools dependency was not added under the 'waf-tools'
      name.
   3) The waf-tools were not bundled using the --bundle=.. and
      related functions.
"""
@conf
def load_external_tool(conf,category,name):
	if not conf.has_dependency_path('waf-tools'):
		conf.fatal(load_error)
	path=conf.dependency_path('waf-tools')
	conf.load([name],tooldir=[os.path.join(path,category)])
