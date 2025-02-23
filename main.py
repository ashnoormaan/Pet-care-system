from fastapi import FastAPI
from router import router

app = FastAPI()

# Include all routes
app.include_router(router)

@app.get("/")
def home():
    return {"message": "Welcome to the Pet Care API"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run (app, host="127.0.0.1", port=8000 )