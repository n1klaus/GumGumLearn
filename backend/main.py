#!/usr/bin/python3
"""Module to define uvicorn server instance"""
import uvicorn
import asyncio
from watchfiles import awatch
from os import getenv

# async def main():
#     """Include directories to watch for changes"""
#     async for changes in awatch("./"):
#         print(changes)

if __name__ == "__main__":
    # asyncio.run(main())
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
