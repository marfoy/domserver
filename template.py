import sys
import codecs
import jinja2

class MyCouple(object):
	def __init__(self, a, b):
		self.t = a
		self.n = b

raw = codecs.open('template.tpl', encoding='utf-8').read()
template = jinja2.Template(raw, trim_blocks=True)
values = dict()
values['mylist'] = [MyCouple(1,2), MyCouple(3,4)]
print template.render(**values).encode('utf-8')
