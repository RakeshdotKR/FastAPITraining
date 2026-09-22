from fastapi import FastAPI
app = FastAPI()
@app.get("/")
def home():
    return {"page":"Home"}

@app.get("/about")
def about():
    return {"page":"About","author":"Rakesh"}

@app.get("/health")
def health():
    return {"status":"ok"}