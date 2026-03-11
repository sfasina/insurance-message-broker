import json
import os
from fastapi import FastAPI
from pydantic import BaseModel
from confluent_kafka import Producer

app = FastAPI()

KAFKA_BROKER = os.getenv('KAFKA_BROKER', 'localhost:9092')

kafka_config = {'bootstrap.servers': KAFKA_BROKER}
producer = Producer(kafka_config)

class Insurance_claim(BaseModel):
   claimer_name: str
   claimer_id_number: int
   contract_number: int
   claim_sum: float  

@app.post("/api/claim")
async def create_claim(user_data: Insurance_claim):
   claim_dict = user_data.model_dump()
   claim_json = json.dumps(claim_dict)
   
   producer.produce('insurance-claims', value=claim_json.encode('utf-8'))  
   producer.flush()
   
   print(f"Claim from {user_data.claimer_name} was sent to Kafka: {claim_json}")
   
   return {"status": "accepted", "message": "Insurance claim was successfully sent to Kafka"}