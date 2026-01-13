# monitoring/detection.py

def detect_attack(data):
    """
    Dummy attack detection.
    Returns:
        attack (str): attack type or None
        anomaly (bool): True if any anomaly detected
    """
    anomaly = any(d.anomaly for d in data)
    attack = "FDI Attack" if anomaly else None
    return attack, anomaly

