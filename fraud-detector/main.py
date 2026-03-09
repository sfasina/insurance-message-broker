import json
from confluent_kafka import Consumer


conf = {
   'bootstrap.servers': 'localhost:9092',
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
      claim_data = json.loads(claim_data_json)
      
      print("-" * 40)

      print("Checking for missing information.")
      
      if claim_data['claimer_name'] is None:
         print("Missing claimer name.")
      elif claim_data['claimer_id_number'] is None:
         print("Missing claimer ID number.")
      elif claim_data['contract_number'] is None:
         print("Missing contract number.")
      elif claim_data['claim_sum'] is None:
         print("Missing claim sum.")


      print(f"Fraud check for client: {claim_data['claimer_name']}")
      print(f"Contract number: {claim_data['contract_number']}")
      
      if claim_data['claim_sum'] > 50000:
            print("Claim amount exceeds threshold. Potential fraud detected")
      else:
            print("Claim amount was accepted.")
            
except KeyboardInterrupt:
   pass
finally:
   print("Vypínám Fraud Detectora...")
   consumer.close()
