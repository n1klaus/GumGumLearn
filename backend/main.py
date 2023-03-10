#!/usr/bin/python3
"""Module to define uvicorn server instance"""

from dotenv import load_dotenv
from os import getenv, path
import uvicorn

dotenv_path = path.join(path.dirname(__file__), '.env')
load_dotenv(dotenv_path)

if __name__ == "__main__":
    HOST = getenv("GUMGUMLEARN_API_HOST", "0.0.0.0")
    PORT = int(getenv("GUMGUMLEARN_API_PORT", 8000))
    DEV_CONFIG = uvicorn.Config("api.v1.app:app", host=HOST, port=PORT,
                                interface="asgi3",
                                date_header=True,
                                server_header=True,
                                reload=True,
                                reload_dirs=["./"],
                                reload_excludes=["__pycache__/"],
                                log_level="debug"
                                )
    # PROD_CONFIG = uvicorn.Config("api.v1.app:app", host=HOST, port=PORT,
    #                              interface="asgi3",
    #                              workers=2,
    #                              log_level="error"
    #                              )
    server = uvicorn.Server(DEV_CONFIG)
    server.run()
