from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse

app = FastAPI()
templates = Jinja2Templates(directory="./templates")

@app.get("/", response_class=HTMLResponse)
async def get_chat(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

# @app.post("/chat/")
# async def post_chat(request: Request):
#     # form_data = await request.form()
#     # user_input = form_data.get("user_input")
#     # bot_response = get_bot_response(user_input)
#     return {"user_input": user_input, "bot_response": bot_response}

# def get_bot_response(input_text):
#     if "hello" in input_text.lower():
#         return "Hello there!"
#     elif "help" in input_text.lower():
#         return "How can I assist you?"
#     return "I'm not sure how to respond to that."

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app)