from fastapi import FastAPI
from router import router
from database import engine, Base, SessionLocal  # ✅ Import Base here
import threading
import time
from crud import update_expired_availability
from database import initialize_database

app = FastAPI()
# Ensure database schema is updated
# Base.metadata.create_all(engine)

def run_expiry_updates():
    """Runs expired availability check every 5 minutes."""
    while True:
        db = SessionLocal()
        update_expired_availability(db)
        db.close()
        time.sleep(300)

# Start background thread
threading.Thread(target=run_expiry_updates, daemon=True).start()

# Include all routes
app.include_router(router)

@app.get("/")
def home():
    return {"message": "Welcome to the Pet Care API"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="127.0.0.1", port=8080, reload=True)
