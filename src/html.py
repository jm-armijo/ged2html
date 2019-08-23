class HTMLDocument():
	def __init__(self, file_name):
		self.file_name = file_name

	def generate(self, title, tree):
		head = self._getHead(title)
		body = self._getBody(tree)
		html = self._getHTML(head, body)

		file_handler = open(self.file_name, 'w')
		file_handler.write(html)
		file_handler.close()

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
			'  <script>\n'
			'    window.addEventListener(\n'
			'      load",\n'
			'      function() {{\n'
			'        "use strict";\n'
			'{}'
			'      }}\n'
			'    );\n'
			'  </body>'
		).format(body, '')
