import uvicorn

if __name__ == "__main__":
    uvicorn.run(
        "api_service:api_service", host="0.0.0.0", port=8888, log_level="info",
        reload=True, workers=1, reload_dirs=['/code', '/base'],
    )
