from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from extract_pdf import extract_text_from_pdf
from llm_structurer import get_structured_output

app = FastAPI()
# TOGETHER_API_KEY = "af8affb443669b23360116602f15aea7982a51722d8d9b5cc130b15b8961650f"  # replace with real key


# CORS (Allow React frontend to talk to backend)
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",         # for local dev
        "https://pdf-extractor-ui.onrender.com",      # your deployed frontend URL
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/extract")
async def extract(file: UploadFile = File(...)):
    # Step 1: Extract text from PDF
    raw_text = extract_text_from_pdf(file.file)

    # Step 2: Get structured output from Together.ai
    structured_json = get_structured_output(raw_text)

    return structured_json
