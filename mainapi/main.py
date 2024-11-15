from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

class TextRequest(BaseModel):
    text: str

class TextResponse(BaseModel):
    text: str

@app.post("/echo", response_model=TextResponse)
async def echo_text(request: TextRequest):
    # Your logic here
    text = request.text
    
    return TextResponse(text=text)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app)
