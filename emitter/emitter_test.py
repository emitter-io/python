import pytest
try:
    from .emitter import Client
except ImportError:
    from emitter import Client

def test_format_channel():
    tests = [
        {"key": "5xZjIQp6GA9fpxso1Kslqnv8d4XVWCha", "channel": "test", "options": None, "expected": "5xZjIQp6GA9fpxso1Kslqnv8d4XVWCha/test/"},
        {"key": "5xZjIQp6GA9fpxso1Kslqnv8d4XVWCha", "channel": "test/", "options": None, "expected": "5xZjIQp6GA9fpxso1Kslqnv8d4XVWCha/test/"},
        {"key": "5xZjIQp6GA9fpxso1Kslqnv8d4XVWCha/", "channel": "test", "options": None, "expected": "5xZjIQp6GA9fpxso1Kslqnv8d4XVWCha/test/"},
        {"key": "5xZjIQp6GA9fpxso1Kslqnv8d4XVWCha/", "channel": "test/", "options": None, "expected": "5xZjIQp6GA9fpxso1Kslqnv8d4XVWCha/test/"},
        # With options.
        {"key": "5xZjIQp6GA9fpxso1Kslqnv8d4XVWCha", "channel": "test", "options": {Client.with_ttl(5)}, "expected": "5xZjIQp6GA9fpxso1Kslqnv8d4XVWCha/test/?ttl=5"},
        # The following test won't always work, since the enumeration of the options vary in order.
        #{"key": "5xZjIQp6GA9fpxso1Kslqnv8d4XVWCha", "channel": "test", "options": {Client.with_ttl(5), Client.without_echo()}, "expected": "5xZjIQp6GA9fpxso1Kslqnv8d4XVWCha/test/?ttl=5&me=0"}
        ]
    
    for test in tests:
        formatted = Client._format_channel(key=test["key"], channel=test["channel"], options=test["options"])  
        assert formatted == test["expected"]

def test_format_channel_link():
    tests = [
        {"channel": "test", "options": {Client.with_ttl(5)}, "expected": "test/?ttl=5"},
        ]
    
    for test in tests:
        formatted = Client._format_channel_link(channel=test["channel"], options=test["options"])  
        assert formatted == test["expected"]

# Todo test shared
