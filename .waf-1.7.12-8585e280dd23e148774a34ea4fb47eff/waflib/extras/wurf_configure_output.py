#! /usr/bin/env python
# encoding: utf-8
# WARNING! Do not edit! http://waf.googlecode.com/git/docs/wafbook/single.html#_obtaining_the_waf_file

import os,sys,inspect,ast
from waflib import Utils
from waflib import Context
from waflib import Options
from waflib import Errors
from waflib.Configure import conf
from waflib.Configure import ConfigurationContext
class ToolchainConfigurationContext(ConfigurationContext):
	'''configures the project'''
	cmd='configure'
	def init_dirs(self):
		assert(getattr(Context.g_module,Context.OUT,None)==None)
		if not Options.options.out:
			if self.has_tool_option('cxx_mkspec'):
				mkspec=self.get_tool_option('cxx_mkspec')
				self.out_dir=os.path.join("build",mkspec)
			else:
				build_platform=Utils.unversioned_sys_platform()
				self.out_dir=os.path.join("build",build_platform)
			if self.has_tool_option('cxx_debug'):
				self.out_dir+='_debug'
		super(ToolchainConfigurationContext,self).init_dirs()
