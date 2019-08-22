class HTMLDocument():
	def __init__(self, title, body):
		self.title = title
		self.body = body

	def getHTML(self):
		head = self._getHead()
		body = self._getBody()
		html = (
			'<!doctype html>\n'
			'<html lang="en">\n'
			'{}\n'
			'{}\n'
			'</html>'
		).format(head, body)

		return html
	def _getHead(self):
		header = (
			'  <head>\n'
			'    <meta charset="utf-8">\n'
			'    <title>{}</title>\n'
			'    <link rel="stylesheet" href="../css/styles.css">\n'
			'  </head>'
		).format(self.title)

		return header
	
	def _getBody(self):
		body = (
			'  <body>\n'
			'{}\n'
			'  </body>'
		).format(self.body)

		return body

