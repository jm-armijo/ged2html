class HTMLGenerator():
	def __init__(self, file_name):
		self.file_name = file_name

	def generate(self, title, tree):
		head = self._getHead(title)
		body = self._getBody(tree)
		html = self._getHTML(head, body)

		file_handler = open(self.file_name, 'w')
		file_handler.write(html)
		file_handler.close()

	@staticmethod
	def wrap(instance, value, id=''):
		class_name = type(instance).__name__.lower()
		attributes = HTMLGenerator._getAttributes(class_name, id)

		return (
			'<div {}>\n'
			'{}\n'
			'</div>\n'
		).format(attributes, value)

	@staticmethod
	def listToHTML(items):
		html = ''
		for item in items:
			html += item.toHTML()
		return html

	@staticmethod
	def getOnLoadScript(script):
		return (
			'  <script>\n'
			'    window.addEventListener(\n'
			'      "load",\n'
			'      function() {{\n'
			'        "use strict";\n'
			'{}'
			'      }}\n'
			'    );\n'
			'  </script>'
		).format(script)

	@staticmethod
	def _getAttributes(class_name, id):
		tag = list()
		tag.append('class="{}"'.format(class_name))
		tag.append('id="{}"'.format(id)) if id != '' else ''
		return " ".join(tag)

	def _getHTML(self, head, body):
		return (
			'<!doctype html>\n'
			'<html lang="en">\n'
			'{}\n'
			'{}\n'
			'</html>'
		).format(head, body)

	def _getHead(self, title):
		return (
			'  <head>\n'
			'    <meta charset="utf-8">\n'
			'    <title>{}</title>\n'
			'    <link rel="stylesheet" href="css/styles.css">\n'
			'    <script src="scripts/leader-line.min.js"></script>\n'
			'  </head>'
		).format(title)
	
	def _getBody(self, body):
		return (
			'  <body>\n'
			'{}\n'
			'  </body>'
		).format(body, '')
