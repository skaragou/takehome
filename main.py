from fastapi import FastAPI,HTTPException
from contextlib import asynccontextmanager
import transformers
import torch
import json
import yaml
import uvicorn

session = {}

@asynccontextmanager
async def startup(app: FastAPI):

    # Load config file which has prompt for LLM.
    with open('./config.yaml', 'r') as f:
        config = yaml.safe_load(f)

    pipeline = transformers.pipeline(
        "text-generation",
        model=config['hugging_face_model'],
        model_kwargs={"torch_dtype": torch.bfloat16},
        device_map="auto",
    )
    session['pipeline'] = pipeline
    session['prompt'] = config['llm_prompt']
    yield
    session.clear()

app = FastAPI(lifespan=startup)

def model_prediction(clinical_text: str) -> list[str]:
    messages = [
        {'role': 'system', 'content': session['prompt']},
        {'role': 'user', 'content': clinical_text}
    ]
    outputs = session['pipeline'](
        messages,
        max_new_tokens=256,
    )
    json_array = outputs[0]["generated_text"][-1]
    return json.loads(json_array)


@app.get("/{clinical_text}")
async def read_root(clinical_text:str):
    if not clinical_text: 
        raise HTTPException(status_code=418, detail="Please provide text")
    
    json_blob = json.loads(clinical_text)

    if not 'clinical_note' in json_blob:
        raise HTTPException(status_code=418, detail="Please provide a clinical node of the format \{\"clinical_note\": \"[YOUR TEXT HERE.]\"\}")

    model_output = model_prediction(clinical_text)
    return {'diagnoses': model_output}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=3000, log_level="info")