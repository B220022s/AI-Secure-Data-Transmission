import hashlib
import json

class AIDataGuardian:
    def __init__(self, secret_key):
        self.secret_key = secret_key

    def create_packet(self, data):
        guard_signature = hashlib.sha256(f"{data}{self.secret_key}".encode()).hexdigest()
        return json.dumps({
            "payload": data,
            "guard": guard_signature
        })

    def verify_packet(self, packet):
        packet_data = json.loads(packet)
        expected_guard = hashlib.sha256(f"{packet_data['payload']}{self.secret_key}".encode()).hexdigest()
        if packet_data["guard"] != expected_guard:
            return False  # Tampering detected!
        return True

# Example Usage
guardian = AIDataGuardian("MY_SECRET_KEY")
packet = guardian.create_packet("Sensitive Information")
print(guardian.verify_packet(packet))  # True

# Simulate tampering
tampered_packet = json.loads(packet)
tampered_packet["payload"] = "Hacked Data"
tampered_packet = json.dumps(tampered_packet)
print(guardian.verify_packet(tampered_packet))  # False
