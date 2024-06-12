import random
import string
import time
import uuid

class Publisher:
    def __init__(self, id):
        self.id = id
        self.running = True  # Variable to control the running state

    def generate_publication(self):
        content = ''.join(random.choices(string.ascii_letters + string.digits, k=19)) + 'A'
        content = ''.join(random.sample(content, len(content)))  # Randomize the order of characters
        return {
            'id': str(uuid.uuid4()),  # Unique identifier for the publication
            'publisher_id': self.id,
            'content': content,
            'timestamp': time.time()
        }

    def start_publishing(self, broker, interval=1):
        while self.running:
            publication = self.generate_publication()
            broker.publish(publication)
            time.sleep(interval)
    
    def stop_publishing(self):
        self.running = False  # Method to stop publishing
