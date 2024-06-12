import time


class Subscriber:
    def __init__(self, id):
        self.id = id
        self.received_publications = []

    def notify(self, publication):
       latency = time.time() - publication['timestamp']
       self.received_publications.append((publication, latency))
       print(f"Subscriber {self.id} received publication: {publication} with latency {latency:.4f} seconds")

    def subscribe(self, broker, filter_func):
        broker.subscribe({'subscriber': self, 'filter': filter_func})

    def get_average_latency(self):
        if not self.received_publications:
            return 0
        total_latency = sum(latency for _, latency in self.received_publications)
        return total_latency / len(self.received_publications)
