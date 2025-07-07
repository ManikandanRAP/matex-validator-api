from fastapi import FastAPI
from app.api.endpoints import notifications

app = FastAPI(
    title="MatEx RAP Validator Integration API",
    description="API for receiving real-time notifications from the MatEx Portal.",
    version="1.0.0"
)

app.include_router(notifications.router, tags=["Notifications"])

@app.get("/")
def read_root():
    return {"message": "Welcome to the MatEx RAP Validator Integration API"}
