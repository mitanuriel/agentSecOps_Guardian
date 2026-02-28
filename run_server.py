"""Start the AgentOps Guardian social media manager server."""

import uvicorn

if __name__ == "__main__":
    uvicorn.run(
        "src.social_media_backend:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )
