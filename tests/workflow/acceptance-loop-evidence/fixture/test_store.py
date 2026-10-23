import unittest
from store import SessionStore


class StoreTests(unittest.TestCase):
    def test_account_switch(self):
        store = SessionStore()
        store.set_user("a")
        store.put("record", "private")
        store.set_user("b")
        self.assertIsNone(store.get("record"))


if __name__ == "__main__":
    unittest.main()
