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

# POST request
@app.post("/create")
def create_something():
    return {"message":"Created"}

# Path Parameters
@app.get("/student/{usn}")
def get_result(usn):
    return {"Result":"Distinction","usn":usn}

# Path Parameters with Type Hint
@app.get("/candidate/{rollno}")
def get_candidate(rollno:int):
    return {"Result":"Distinction","rollno":rollno,"type":str(type(rollno))}