from fastapi import FastAPI
from router import router
from database import engine, Base  # ✅ Import Base here

app = FastAPI()

# ✅ Create database tables only once
Base.metadata.create_all(bind=engine)

# Include all routes
app.include_router(router)

@app.get("/")
def home():
    return {"message": "Welcome to the Pet Care API"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="127.0.0.1", port=8080, reload=True)
