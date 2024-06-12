import random
import threading
import time
from publisher import Publisher
from broker import AdvancedBroker
from subscriber import Subscriber

def run_test():
    # Create brokers
    broker1 = AdvancedBroker(1)
    broker2 = AdvancedBroker(2)
    broker3 = AdvancedBroker(3)

    # Link brokers
    broker1.add_neighbor(broker2)
    broker2.add_neighbor(broker3)
    broker3.add_neighbor(broker1)

    # Create publishers
    publisher1 = Publisher(1)
    publisher2 = Publisher(2)
    
    # Start publishing in separate threads
    publisher1_thread = threading.Thread(target=publisher1.start_publishing, args=(broker1, 0.1))  # Publish every 0.1 seconds
    publisher2_thread = threading.Thread(target=publisher2.start_publishing, args=(broker2, 0.1))
    publisher1_thread.start()
    publisher2_thread.start()

    # Create subscribers
    subscribers = [Subscriber(i) for i in range(1, 10001)]

    # Define filter functions for 100% equality scenario
    filter_func1 = lambda pub: 'A' in pub['content']
    
    # Subscribe all subscribers to broker1 for 100% equality scenario
    for sub in subscribers[:5000]:
        sub.subscribe(broker1, filter_func1)

    # Define filter functions for 25% equality scenario
    filter_func2 = lambda pub: random.choice([True, False, False, False]) and 'A' in pub['content']
    
    # Subscribe all subscribers to broker2 for 25% equality scenario
    for sub in subscribers[5000:]:
        sub.subscribe(broker2, filter_func2)

    # Let the system run for 3 minutes
    run_time = 180  # 3 minutes in seconds
    time.sleep(run_time)

    # Stop publishers
    publisher1.stop_publishing()
    publisher2.stop_publishing()

    # Wait for publisher threads to finish
    publisher1_thread.join()
    publisher2_thread.join()

    # Collect statistics
    delivered_publications = broker1.get_delivered_publications_count() + broker2.get_delivered_publications_count() + broker3.get_delivered_publications_count()
    total_latencies = sum(sub.get_average_latency() for sub in subscribers if sub.received_publications)
    total_received_publications = sum(len(sub.received_publications) for sub in subscribers)
    
    if total_received_publications > 0:
        average_latency = total_latencies / total_received_publications
    else:
        average_latency = 0

    match_rate_100 = sum(len(sub.received_publications) for sub in subscribers[:5000]) / 5000
    match_rate_25 = sum(len(sub.received_publications) for sub in subscribers[5000:]) / 5000

    # Print statistics
    print(f"Total delivered publications: {delivered_publications}")
    print(f"Average latency: {average_latency:.4f} seconds")
    print(f"Match rate for 100% equality: {match_rate_100:.4f}")
    print(f"Match rate for 25% equality: {match_rate_25:.4f}")

if __name__ == "__main__":
    run_test()
