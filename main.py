from fastapi import FastAPI, File, UploadFile, Form
from fastapi.responses import JSONResponse
from gemini_client import get_nutrition_info_from_file
from fastapi.middleware.cors import CORSMiddleware


app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/ping")
def ping():
    return {"message": "pong"}



"""
POST /upload_image/

Accepts an image and optional description of food, and returns nutritional insights using Gemini Flash.

Request (multipart/form-data):
- file: Required image file (JPG/PNG)
- description: Optional string describing the food (e.g., "biryani with curd")

Returns:
- JSON response with estimated nutritional information:

{
    "calories": "450 kcal",
    "protein": "15g",
    "fat": "12g",
    "carbs": "65g",
    "additional_info": "Based on a standard serving",
    "summary": "Balanced meal with moderate carbs",
    "score": 85
}

Errors:
- 422 if file is missing
- 500 if Gemini returns invalid response
"""


@app.post("/upload_image/")
async def analyze_image(
    file: UploadFile = File(...),
    description: str = Form(default="")  # Optional description
):
    contents = await file.read()
    result = get_nutrition_info_from_file(contents, description)
    return JSONResponse(content=result)





@app.get("/", summary="Welcome")
async def root():
    return {
        "message": "Welcome to the Krave AI Backend!",
        "docs": "/docs",
        "upload_endpoint": "/upload_image/",
        "health check": "/ping"
    }
