import asyncio
import tornado
from jinja2 import Template
from cogs.setup import properties, save_properties
from icecream import ic 
from cogs.punishsystem import entbannen

class FileHandler(tornado.web.RequestHandler):
    def get(self, path, ext):
        path = f"webserver/{path}"

        if ext == 'png':
            self.set_header("Content-Type", "image/png")
        if ext == 'svg':
            self.set_header("Content-Type", "image/svg+xml")
        if ext == 'css':
            self.set_header("Content-Type", "text/css")

        try:
            with open(path, 'rb') as file:
                ic(file)
                self.write(file.read())
        except FileNotFoundError:
            ic("not found")
            return None

class MainHandler(tornado.web.RequestHandler):
    def get(self):
        unban_token = self.get_query_argument('unban_token', default=None)
        user_name = None
        user_id = None

        ic(self.request.uri)

        for bu in properties['banned-users']:
            if unban_token == bu['unban_token']:
                user_name = bu['name']
                user_id = bu['id']

        if user_name == None:
            with open('webserver/error.html') as file:
                page = Template(file.read()).render()
        else:    
            with open('webserver/index.html.j2', 'r',encoding="utf-8") as file:
                page = Template(file.read()).render(
                    user_name = user_name,
                    user_id = user_id
                )

        self.write(page)
    
    async def post(self):
        self.set_header("Content-Type", "text/plain")
        grund = self.get_body_argument("grund")
        user_id = self.get_body_argument("user_id")
        await entbannen(user_id, grund)


def make_app():
    return tornado.web.Application([
        (r"/resources/(.*)", tornado.web.StaticFileHandler, {"path": "./webserver/resources"}),
        (r"/", MainHandler),
    ])

async def webserver_main():
    app = make_app()
    app.listen(8888)
    await asyncio.Event().wait()


