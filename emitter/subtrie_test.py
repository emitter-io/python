import pytest
from subtrie import SubTrie


def test_lookup_with_wildcard():
    t = SubTrie()
    t.insert("a/", lambda: None)
    t.insert("a/b/c/", lambda: None)
    t.insert("a/+/c/", lambda: None)
    t.insert("a/b/c/d/", lambda: None)
    t.insert("a/+/c/+/", lambda: None)
    t.insert("x/", lambda: None)
    t.insert("x/y/", lambda: None)
    t.insert("x/+/z/", lambda: None)

    tests =	{
        "a/": 1,
		"a/1/": 1,
		"a/2/": 1,
		"a/1/2/": 1,
		"a/1/2/3/": 1,
		"a/x/y/c/": 1,
		"a/x/c/": 2,
		"a/b/c/": 3,
		"a/b/c/d/": 5,
		"a/b/c/e/": 4,
		"x/y/c/e/": 2}

    for k, v in tests.items():
        results = t.lookup(k)
        assert len(results) == v


def test_delete_parent():
    t = SubTrie()
    t.insert("a", lambda: None)
    t.insert("a/b/c", lambda: None)
    t.insert("a/+/c", lambda: None)

    t.delete("a")

    results = t.lookup("a")
    assert len(results) == 0

    results = t.lookup("a/b")
    assert len(results) == 0
    
    results = t.lookup("a/b/c")
    assert len(results) == 2

def test_delete_child():
    t = SubTrie()
    t.insert("a", lambda: None)
    t.insert("a/b", lambda: None)

    results = t.lookup("a/b")
    assert len(results) == 2

    t.delete("a/b")

    results = t.lookup("a/b")
    assert len(results) == 1

def test_delete_inexistent_child():
    t = SubTrie()
    t.insert("a", lambda: None)
    t.insert("a/b", lambda: None)

    t.delete("c")

    results = t.lookup("a/b")
    assert len(results) == 2


def test_delete_root():
    t = SubTrie()
    t.insert("a", lambda: None)

    t.delete("a")

    results = t.lookup("a")
    assert len(results) == 0