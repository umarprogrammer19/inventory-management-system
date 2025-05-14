import time
import random

def simulate_payment():
    """Simulate a payment process."""
    # In a real application, this would connect to a payment gateway
    # For demo purposes, we'll just simulate a payment with a 90% success rate
    time.sleep(1)  # Simulate processing time
    return random.random() < 0.9  # 90% success rate