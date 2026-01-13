from .models import GridData
from django.utils import timezone
from datetime import timedelta

def detect_attack(data):
    """Check for anomalies in the latest data"""
    if not data:
        return None, False

    latest = data[-1]
    attack = None
    anomaly = False

    # Rule 1: False Data Injection (FDI) if voltage out of range
    if latest.voltage < 200 or latest.voltage > 250:
        attack = "False Data Injection (FDI)"
        anomaly = True

    # Rule 2: Replay Attack (if last 3 readings are identical)
    if len(data) >= 3:
        if data[-1].voltage == data[-2].voltage == data[-3].voltage:
            attack = "Replay Attack"
            anomaly = True

    # Rule 3: DoS Attack (if no update for > 10 seconds)
    if len(data) >= 2:
        gap = (data[-1].timestamp - data[-2].timestamp).total_seconds()
        if gap > 10:
            attack = "Denial of Service (DoS)"
            anomaly = True

    if anomaly:
        latest.anomaly = True
        latest.attack_type = attack
        latest.save()

    return attack, anomaly

