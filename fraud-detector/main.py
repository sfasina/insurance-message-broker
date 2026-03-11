import json
import os
from confluent_kafka import Consumer


KAFKA_BROKER = os.getenv('KAFKA_BROKER', 'localhost:9092')

conf = {
   'bootstrap.servers': KAFKA_BROKER,
   'group.id': 'fraud-detection-group',
   'auto.offset.reset': 'earliest'
}

consumer = Consumer(conf)


consumer.subscribe(['insurance-claims'])

print("Fraud Detector started, waiting for insurance claims...")


try:
   while True:
      msg = consumer.poll(timeout=1.0)
      
      if msg is None:
         continue
            
      if msg.error():
         print(f"Error reading from Kafka: {msg.error()}")
         continue

      
      claim_data_json = msg.value().decode('utf-8')
      
      try:
         claim_data = json.loads(claim_data_json)
      except json.JSONDecodeError as error:
         print(f"Invalid JSON: {error}. Skipping.")
         continue
      
      print("-" * 40)

      print("Checking for missing information.")
      
      required_fields = ["claimer_name", "claimer_id_number", "contract_number", "claim_sum"]
      missing = [field for field in required_fields if claim_data.get(field) is None]

      if missing:
         print(f"Missing fields: {', '.join(missing)}")
         continue


      print(f"Fraud check for client: {claim_data.get('claimer_name')}")
      print(f"Contract number: {claim_data.get('contract_number')}")
      
      if claim_data.get('claim_sum') > 50000:
            print("Claim amount exceeds threshold. Potential fraud detected")
      else:
            print("Claim amount was accepted.")
            
except KeyboardInterrupt:
   pass
finally:
   print("Vypínám Fraud Detectora...")
   consumer.close()
