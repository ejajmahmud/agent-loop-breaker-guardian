"""Core Agent Loop Breaker Guardian implementation."""
import hashlib
from typing import Dict, List, Optional, Tuple, Any


class LoopIntervention:
    def __init__(self, loop_detected: bool, period: int = 0, message: str = ""):
        self.loop_detected = loop_detected
        self.period = period
        self.message = message


class LoopBreakerGuardian:
    def __init__(self, max_history: int = 15, repeat_threshold: int = 2):
        self.max_history = max_history
        self.repeat_threshold = repeat_threshold
        self.history_hashes: List[str] = []
        self.error_hashes: List[str] = []

    def compute_action_hash(self, tool_name: str, payload_str: str) -> str:
        norm = f"{tool_name.strip().lower()}::{payload_str.strip()}"
        return hashlib.sha256(norm.encode()).hexdigest()[:16]

    def record_step(self, tool_name: str, payload_str: str, error_msg: Optional[str] = None) -> LoopIntervention:
        action_h = self.compute_action_hash(tool_name, payload_str)
        self.history_hashes.append(action_h)
        if error_msg:
            err_h = hashlib.sha256(error_msg.strip().encode()).hexdigest()[:16]
            self.error_hashes.append(err_h)

        if len(self.history_hashes) > self.max_history:
            self.history_hashes.pop(0)

        # Check consecutive identical actions
        if len(self.history_hashes) >= 2 and self.history_hashes[-1] == self.history_hashes[-2]:
            return LoopIntervention(True, 1, "Immediate repetition of identical action detected.")

        # Check period-2 oscillation (A -> B -> A -> B)
        if len(self.history_hashes) >= 4:
            if self.history_hashes[-1] == self.history_hashes[-3] and self.history_hashes[-2] == self.history_hashes[-4]:
                return LoopIntervention(True, 2, "Period-2 oscillation detected: alternating between two conflicting actions.")

        # Check identical error repeated N times
        if len(self.error_hashes) >= self.repeat_threshold:
            if len(set(self.error_hashes[-self.repeat_threshold:])) == 1:
                return LoopIntervention(True, 0, f"Identical error repeated {self.repeat_threshold} times consecutively.")

        return LoopIntervention(False)

    def reset(self):
        self.history_hashes.clear()
        self.error_hashes.clear()
