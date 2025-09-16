from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
import logging
from fastapi.responses import JSONResponse
from routes import (
    mensajes)
from fastapi.exceptions import RequestValidationError
import uvicorn

agentic_api = FastAPI(title="AGW")

# Logging
logging.basicConfig(level=logging.DEBUG)
logging.getLogger('sqlalchemy.engine').setLevel(logging.WARNING)
logging.getLogger("urllib3").setLevel(logging.WARNING)
logging.getLogger('sqlalchemy.engine.Engine').setLevel(logging.WARNING)
logging.getLogger('sqlalchemy.pool').setLevel(logging.WARNING)
logging.getLogger("python_multipart.multipart").setLevel(logging.WARNING)
logging.getLogger("httpcore").setLevel(logging.WARNING)
logging.getLogger("httpx").setLevel(logging.WARNING)
logging.getLogger("openai").setLevel(logging.WARNING)
logging.getLogger('botocore').setLevel(logging.WARNING)
logging.getLogger("azure.core.pipeline.policies.http_logging_policy").setLevel(logging.WARNING)
logging.getLogger("filelock").setLevel(logging.WARNING)

agentic_api.include_router(mensajes.router)

if __name__ == "__main__":
    uvicorn.run(
        "main:agentic_api",  
        host="0.0.0.0",
        port=7000
 #       ssl_certfile=cert_path,
 #       ssl_keyfile=key_path
    )
