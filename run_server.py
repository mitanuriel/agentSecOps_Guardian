"""Start the AgentOps Guardian social media manager server."""

import os
import uvicorn

if __name__ == "__main__":
    # Read configuration from environment variables with safer defaults
    host = os.getenv("BIND_HOST", "127.0.0.1")
    port = int(os.getenv("BIND_PORT", "8000"))
    reload = os.getenv("BIND_RELOAD", "false").lower() in ("true", "1", "yes")
    
    uvicorn.run(
        "src.social_media_backend:app",
        host=host,
        port=port,
        reload=reload,
        log_level="info"
    )
