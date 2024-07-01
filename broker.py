class Broker:
    def __init__(self, id):
        self.id = id
        self.subscriptions = []
        self.neighbors = []
        self.delivered_publications = 0  # Count of successfully delivered publications

    def add_neighbor(self, broker):
        self.neighbors.append(broker)

    def subscribe(self, subscription):
        self.subscriptions.append(subscription)

    def publish(self, publication):
        for subscription in self.subscriptions:
            if subscription['filter'](publication):
                subscription['subscriber'].notify(publication)
                self.delivered_publications += 1  # Increment successful delivery count
        for neighbor in self.neighbors:
            neighbor.publish(publication)

    def get_delivered_publications_count(self):
        return self.delivered_publications

class AdvancedBroker(Broker):
    def __init__(self, id):
        super().__init__(id)
        self.processed_publications = set()

    def publish(self, publication):
        publication_id = publication.get('id')
        if publication_id in self.processed_publications:
            return  # Avoid processing the same publication multiple times

        self.processed_publications.add(publication_id)
        
        # Notify local subscribers
        for subscription in self.subscriptions:
            if subscription['filter'](publication):
                subscription['subscriber'].notify(publication)
                self.delivered_publications += 1  # Increment successful delivery count
        
        # Propagate to neighbors
        for neighbor in self.neighbors:
            neighbor.publish(publication)
