import pickle
from fastapi import FastAPI
import uvicorn
from typing import Literal
from pydantic import BaseModel, Field


# Load the pipeline
with open("pipeline_v1.bin", "rb") as f:
    model = pickle.load(f)

# Define the input schema
class Client(BaseModel):
    lead_source: str
    number_of_courses_viewed: int = Field(..., ge=0)
    annual_income: float = Field(..., ge=0.0)

class PredictResponse(BaseModel):
    subscription_probability: float

# Create the app
app = FastAPI()

@app.post("/predict")
def predict(client: Client) -> PredictResponse:
    X = [client.dict()]
    proba = model.predict_proba(X)[0, 1]
    return PredictResponse(subscription_probability=proba)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=9696)
