from aiohttp import web

from web.costumer import routes as cos_routes
from web.middleware import error_middleware

app = web.Application(middlewares=[error_middleware])

app.add_routes([*cos_routes])
web.run_app(app)
