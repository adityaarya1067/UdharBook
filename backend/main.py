from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routes import transactions, notes, chat

app = FastAPI(title="UdharBook API", version="1.0.0")

# CORS Configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify your frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(transactions.router, prefix="/api", tags=["Transactions"])
app.include_router(notes.router, prefix="/api", tags=["Notes"])
app.include_router(chat.router, prefix="/api", )

@app.get("/")
async def root():
    return {"message": "Welcome to UdharBook API"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)