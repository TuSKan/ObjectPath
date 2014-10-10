#!/usr/bin/env python
# -*- coding: utf-8 -*-

from objectpath.utils import *
import sys, unittest, os

sys.setrecursionlimit(20000)

class Utils_test(unittest.TestCase):
	def test_Utils_JSON_compat(self):
		from objectpath.utils import json_compat
		self.assertEqual(json_compat.loads("[u'ddd']"),['ddd'])
		#self.assertEqual(json_compat.dumps(['ddd']),'[\n  "ddd"\n]')
		self.assertEqual(py2JSON(False), 'false')
		self.assertEqual(py2JSON(None), 'null')
		self.assertEqual(py2JSON((2,3,4)), [2,3,4])
		if sys.version_info.major < 3:
			self.assertEqual(py2JSON(unicode('')), '')
		self.assertEqual(py2JSON(2), '2')
		self.assertEqual(json_compat.printJSON([1,2,3,4,5,6]), "[\n  \x1b[36m\x1b[1m1\x1b[0m\x1b[0m,\n  \x1b[36m\x1b[1m2\x1b[0m\x1b[0m,\n  \x1b[36m\x1b[1m3\x1b[0m\x1b[0m,\n  \x1b[36m\x1b[1m4\x1b[0m\x1b[0m,\n  \x1b[36m\x1b[1m5\x1b[0m\x1b[0m,\n  ... (1 more items)\n]")
		self.assertEqual(json_compat.printJSON([{},1]), '[\n  {},\n  \x1b[36m\x1b[1m1\x1b[0m\x1b[0m\n]')
		self.assertEqual(json_compat.printJSON({"aaa":1}), '{\x1b[33m\x1b[1m"aaa"\x1b[0m\x1b[0m: \x1b[36m\x1b[1m1\x1b[0m\x1b[0m}')
		self.assertEqual(json_compat.printJSON({"a":[1,2,3]}), '{\x1b[33m\x1b[1m"a"\x1b[0m\x1b[0m: [\n  \x1b[36m\x1b[1m1\x1b[0m\x1b[0m,\n  \x1b[36m\x1b[1m2\x1b[0m\x1b[0m,\n  \x1b[36m\x1b[1m3\x1b[0m\x1b[0m\n]}')
		self.assertEqual(json_compat.printJSON([[1],{"aa":2}]), '[\n  [\x1b[36m\x1b[1m1\x1b[0m\x1b[0m],\n  {\x1b[33m\x1b[1m"aa"\x1b[0m\x1b[0m: \x1b[36m\x1b[1m2\x1b[0m\x1b[0m}\n]')

testcase1=unittest.TestLoader().loadTestsFromTestCase(Utils_test)

utils_test=unittest.TestSuite([testcase1])