"""Unit tests for agent-loop-breaker-guardian."""
import unittest
from agent_loop_breaker_guardian.guardian import LoopBreakerGuardian


class TestLoopBreakerGuardian(unittest.TestCase):
    def setUp(self):
        self.guardian = LoopBreakerGuardian(repeat_threshold=2)

    def test_immediate_repetition(self):
        self.guardian.record_step("tool_a", "args_1")
        res = self.guardian.record_step("tool_a", "args_1")
        self.assertTrue(res.loop_detected)
        self.assertEqual(res.period, 1)

    def test_period_two_oscillation(self):
        self.guardian.record_step("t1", "p1")
        self.guardian.record_step("t2", "p2")
        self.guardian.record_step("t1", "p1")
        res = self.guardian.record_step("t2", "p2")
        self.assertTrue(res.loop_detected)
        self.assertEqual(res.period, 2)

    def test_normal_progression(self):
        res1 = self.guardian.record_step("t1", "p1")
        res2 = self.guardian.record_step("t2", "p2")
        self.assertFalse(res1.loop_detected)
        self.assertFalse(res2.loop_detected)
