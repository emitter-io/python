import pytest
import emitter

def test_formatChannel():
    tests = [
        {"key": "5xZjIQp6GA9fpxso1Kslqnv8d4XVWCha", "channel": "test", "options": None, "expected": "5xZjIQp6GA9fpxso1Kslqnv8d4XVWCha/test/"},
        {"key": "5xZjIQp6GA9fpxso1Kslqnv8d4XVWCha", "channel": "test/", "options": None, "expected": "5xZjIQp6GA9fpxso1Kslqnv8d4XVWCha/test/"},
        {"key": "5xZjIQp6GA9fpxso1Kslqnv8d4XVWCha/", "channel": "test", "options": None, "expected": "5xZjIQp6GA9fpxso1Kslqnv8d4XVWCha/test/"},
        {"key": "5xZjIQp6GA9fpxso1Kslqnv8d4XVWCha/", "channel": "test/", "options": None, "expected": "5xZjIQp6GA9fpxso1Kslqnv8d4XVWCha/test/"},
        # With options.
        {"key": "5xZjIQp6GA9fpxso1Kslqnv8d4XVWCha", "channel": "test", "options": {"ttl":5}, "expected": "5xZjIQp6GA9fpxso1Kslqnv8d4XVWCha/test/?ttl=5"},
        {"key": "5xZjIQp6GA9fpxso1Kslqnv8d4XVWCha", "channel": "test", "options": {"ttl":5,"me":0}, "expected": "5xZjIQp6GA9fpxso1Kslqnv8d4XVWCha/test/?ttl=5&me=0"},
        # Links (without a channel key).
        {"key": "", "channel": "test", "options": {"ttl":5,"me":0}, "expected": "test/?ttl=5&me=0"},
        {"key": None, "channel": "test", "options": {"ttl":5,"me":0}, "expected": "test/?ttl=5&me=0"},
        ]
    
    for test in tests:
        formatted = emitter.Emitter._formatChannel(key=test["key"], channel=test["channel"], options=test["options"])  
        assert formatted == test["expected"]
