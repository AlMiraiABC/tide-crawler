from aiohttp import web

from web.costumer import routes as  cos_routes

app = web.Application()

app.add_routes([*cos_routes])
web.run_app(app)
