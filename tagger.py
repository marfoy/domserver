#!/usr/bin/env python
import argparse
import os
import imp

def fetch_lyrics(bundle, plugins):
	f = 'fetch_lyrics'
	for p in plugins:
		if hasattr(p, f):
			r = getattr(p, f)(bundle)
			if r != None:
				return r

def load_plugins(folder):
	plugins = []
	for p in sorted(os.listdir(folder)):
		if p.endswith('.py'):
			m = p[:-3]
			info = imp.find_module(m, [folder])
			plugins.append(imp.load_module(m, *info))
	return plugins


parser = argparse.ArgumentParser(description="page scraper")
#parser.add_argument('filename', nargs='+', help="target file")
parser.add_argument('--info', '-i', action='store_true', help="print info")
parser.add_argument('--verbose', '-v', default=0, action='count', help="verbose mode")
parser.add_argument('--test', '-t', action='store_true', help="run doctest")
args = parser.parse_args()
if args.test:
	import doctest
	doctest.testmod()

failed = False
plugins = load_plugins('plugins') #FIXME
for target in args.filename:
	if len(target):
		failed = failed or process(target)
if failed:
	exit(1)
