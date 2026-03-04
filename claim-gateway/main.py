from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

class Insurance_claim(BaseModel):
   claimer_name: str
   claimer_id_number: int
   contract_number: int
   claim_sum: float  

@app.post("/api/claim")
async def create_claim(user_data: Insurance_claim):
   
   print(f"Claim from {user_data.claimer_name} was created")
   
   return {"status": "accepted", "message": "Insurance claim was successfully sent"}