"""
The package provides a small auxiliary module ``html`` to easily produce HTML tree and save it to a file.
Very strongly inspired by `dominate package <https://github.com/Knio/dominate>`_.
Actually one motivation to create this module was independence on external package and (much more importantly) that I wanted to learn and implement dominate's handy ``with`` tree building.

The usage is (thanks to dominate) very easy:

.. code:: python
	
	doc = HTMLDocument(title="my title")
	with doc.head:
	   meta(charset="utf-8")
	with doc.body:
	   div(id="id-div-1")
	   with div(id="id-div-1",cls="class-div-1"):
	      p(id="p-1")
	      p("text text",cls="p-class")
	docstr = str(doc) # or unicode(doc) in Python 2
	print(docstr)

which produces:

.. code::

	<!DOCTYPE html>
	<html>
	   <head>
	      <title>
	         my title
	      </title>
	      <meta charset="utf-8">
	   </head>
	   <body>
	      <div id="id-div-1"></div>
	      <div class="class-div-1" id="id-div-1">
	         <p id="p-1"></p>
	         <p class="p-class">
	            text text
	         </p>
	      </div>
	   </body>
	</html>
"""

import six

INDENT = "\t"

_with_stack = []

# https://www.w3.org/TR/html5/syntax.html
_VOID_ELEMENTS = frozenset(("area","base","br","col","embed","hr","img","input","link","meta","param","source","track","wbr"))

class HTMLElement:
	"""
	Class representing HTML element
	
	:param str tag: HTML tag of the element (div, img, ...)
	:param str innerHTML: string content of the element
	:param children: list of child :class:`elements <HTMLElement>`
	:type children: list(:class:`HTMLElement`)
	:params dict attrs: 
	
	.. code:: python
	
		HTMLElement("div","some content",cls="class-1")  # div element with text content and class 'class-1' (note using cls= instead of (in python) impossible class=
		HTMLElement("img",alt="alt text",src="some/url") # empty element with attributes
		HTMLElement("div",children=[                     # nested elements
		   HTMLElement("span","some text"),
		   HTMLElement("div",children=[
		      HTMLElement("p","paragraph 1"),
		      HTMLElement("p","paragraph 2"),
		   ])
		])
	
	The module also provides shorthands for all supported HTML tags, e.g. ``div(...)`` is equivalent to ``HTMLElement("div",...)``
	
	HTMLElement provides handy ``with`` construction.
	All the elements created inside ``with`` block are treated as children of the ``with`` initializer (see below).
	
	So the same code as above, but using ``with`` structure and shorthands:
	
	.. code:: python
	
		div("some content",cls="class-1")
		img(alt="alt text",src="some/url")
		elem = div()
		with elem:
		   span("some text")
		   with div():
		      p("paragraph 1")
		      p("paragraph 2")
	"""
	def __init__(self,tag,innerHTML=u"",children=[],**attrs):
		#: tag of the element
		self.tag = tag
		#: inner text
		self.innerHTML = innerHTML
		#: attribute-value dictionary
		self.attrs = {}
		#: list of child elements
		self.children = []
		#: parent element
		self.parent = None
		#
		for ch in children:
			self.appendChild(ch)
		#
		self._updateAttrs(attrs)
		#
		if _with_stack:
			el = _with_stack[-1]
			el.appendChild(self)
	def _updateAttrs(self,attrs):
		old2new = dict(
			cls = "class",
		)
		for k,v in attrs.items():
			if k in old2new:
				k = old2new[k]
			self.attrs[k] = v
	def appendChild(self,elem):
		"""Appends given element to ``self.children``"""
		self.children.append(elem)
		elem.parent = self
	def _tag(self,slash,level,indent,**attrs):
		attrsstr = u""
		if attrs:
			keys = sorted(attrs.keys())
			attrsstr = " " + " ".join('{}="{}"'.format(k,attrs[k]) for k in keys)
		return u"{}<{}{}{}>".format(level*indent,slash,self.tag,attrsstr)
	def _startTag(self,level=0,indent=INDENT):
		return self._tag("",level,indent,**self.attrs)
	def _endTag(self,level=0,indent=INDENT):
		return self._tag("/",level,indent)
	def toLines(self,level=0,indent=INDENT):
		"""
		Returns HTML document lines of the element

		:param int level: level of indentation
		:param str indent: character(s) to be used as indentation
		"""
		indent1,indent2 = [(level+i)*indent for i in (0,1)]
		if self.innerHTML:
			return [
				self._startTag(level),
				u"{}{}".format(indent2,self.innerHTML),
				self._endTag(level),
			]
		if self.children:
			return [self._startTag(level)] + sum((ch.toLines(level=level+1) for ch in self.children),[]) + [self._endTag(level)]
		if self.tag in _VOID_ELEMENTS:
			return [self._startTag(level)]
		return [self._startTag(level) + self._endTag()]
	def __enter__(self):
		assert self.tag != "html"
		if not self.parent and _with_stack:
			el = _with_stack[-1]
			el.appendChild(self)
		_with_stack.append(self)
		return self
	def __exit__(self,tag,value,traceback):
		_with_stack.pop()

class HTMLDocument:
	"""
	Class representing HTMLDocument
	
	:param str title: title to be used


	"""
	def __init__(self,title=u""):
		self.html = HTMLElement("html",children=[
			HTMLElement("head",children=[
				HTMLElement("title",title),
			]),
			HTMLElement("body"),
		])
		head,body = self.html.children
		#: head element
		self.head = head
		#: body element
		self.body = body
	def __unicode__(self):
		lines = ["<!DOCTYPE html>"] + self.html.toLines()
		return u"\n".join(lines)
	__str__ = __unicode__ if six.PY3 else lambda self: unicode(self).encode("utf8")


# https://www.w3schools.com/tags/
_tags = ("a","abbr","acronym","address","applet","area","article","aside","audio","b","base","basefont","bdi","bdo","big","blockquote","body","br","button","canvas","caption","center","cite","code","col","colgroup","data","datalist","dd","del","details","dfn","dialog","dir","div","dl","dt","em","embed","fieldset","figcaption","figure","font","footer","form","frame","frameset","h1","head","header","hr","html","i","iframe","img","input","ins","kbd","label","legend","li","link","main","map","mark","meta","meter","nav","noframes","noscript","object","ol","optgroup","option","output","p","param","picture","pre","progress","q","rp","rt","ruby","s","samp","script","section","select","small","source","span","strike","strong","style","sub","summary","sup","svg","table","tbody","td","template","textarea","tfoot","th","thead","time","title","tr","track","tt","u","ul","var","video","wbr",)

def _defineTagShortcut(tag):
	globals()[tag] = lambda *args, **attrs: HTMLElement(tag,*args,**attrs)

for _tag in _tags:
	_defineTagShortcut(_tag)
