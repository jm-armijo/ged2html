class HTMLGenerator():
	def __init__(self, file_name):
		self.file_name = file_name

	def generate(self, title, tree):
		head = self._get_head(title)
		body = self._get_body(tree)
		html = self._get_html(head, body)

		file_handler = open(self.file_name, 'w')
		file_handler.write(html)
		file_handler.close()

	@staticmethod
	def wrap(instance, value, id=''):
		class_name = type(instance).__name__.lower()
		attributes = HTMLGenerator._get_attributes(class_name, id)

		return (
			'<div {}>\n'
			'{}\n'
			'</div>\n'
		).format(attributes, value)

	@staticmethod
	def list_to_html(items):
		html = ''
		for item in items:
			html += item.to_html()
		return html

	@staticmethod
	def get_on_load_script(script):
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
	def _get_attributes(class_name, id):
		tag = list()
		tag.append('class="{}"'.format(class_name))
		tag.append('id="{}"'.format(id)) if id != '' else ''
		return " ".join(tag)

	def _get_html(self, head, body):
		return (
			'<!doctype html>\n'
			'<html lang="en">\n'
			'{}\n'
			'{}\n'
			'</html>'
		).format(head, body)

	def _get_head(self, title):
		return (
			'  <head>\n'
			'    <meta charset="utf-8">\n'
			'    <title>{}</title>\n'
			'    <link rel="stylesheet" href="css/styles.css">\n'
			'    <script src="scripts/leader-line.min.js"></script>\n'
			'  </head>'
		).format(title)
	
	def _get_body(self, body):
		return (
			'  <body>\n'
			'{}\n'
			'  </body>'
		).format(body, '')
