import unittest
from store import SessionStore


class AcceptanceRound1(unittest.TestCase):
    def test_A_initial_state(self):
        store = SessionStore()
        self.assertIsNone(store.user)
        self.assertEqual(store.cache, {})

    def test_B_set_identity(self):
        store = SessionStore()
        store.set_user("a")
        self.assertEqual(store.user, "a")

    def test_B_same_identity_preserves_all_cache(self):
        store = SessionStore()
        store.set_user("a")
        store.put("first", "private")
        store.put("second", 0)
        store.set_user("a")
        self.assertEqual(store.user, "a")
        self.assertEqual(store.cache, {"first": "private", "second": 0})

    def test_B_different_identity_clears_all_cache(self):
        store = SessionStore()
        store.set_user("a")
        store.put("first", "private")
        store.put("second", 0)
        store.set_user("b")
        self.assertEqual(store.user, "b")
        self.assertEqual(store.cache, {})
        self.assertIsNone(store.get("first"))
        self.assertIsNone(store.get("second"))

    def test_C_put_get_and_overwrite(self):
        store = SessionStore()
        store.set_user("a")
        for value in ("private", 0, False, "", None, {"item": 1}):
            with self.subTest(value=value):
                store.put("record", value)
                self.assertEqual(store.get("record"), value)
                self.assertIn("record", store.cache)

    def test_C_missing_returns_none(self):
        store = SessionStore()
        self.assertIsNone(store.get("missing"))
        store.put("present", "value")
        self.assertIsNone(store.get("missing"))
        self.assertEqual(store.get("present"), "value")

    def test_D_logout_clears_identity(self):
        store = SessionStore()
        store.set_user("a")
        store.put("record", "private")
        store.logout()
        self.assertIsNone(store.user)

    def test_D_logout_clears_all_cache(self):
        store = SessionStore()
        store.set_user("a")
        store.put("first", "private")
        store.put("second", 0)
        store.logout()
        self.assertEqual(store.cache, {})
        self.assertIsNone(store.get("first"))
        self.assertIsNone(store.get("second"))

    def test_D_repeat_logout_keeps_exited_state(self):
        for populated in (False, True):
            with self.subTest(populated=populated):
                store = SessionStore()
                store.set_user("a")
                if populated:
                    store.put("record", "private")
                store.logout()
                store.logout()
                self.assertIsNone(store.user)
                self.assertEqual(store.cache, {})
                self.assertIsNone(store.get("record"))

    def test_E_same_user_relogin_has_no_previous_cache(self):
        store = SessionStore()
        store.set_user("a")
        store.put("first", "private")
        store.put("second", 0)
        store.logout()
        store.set_user("a")
        self.assertEqual(store.user, "a")
        self.assertEqual(store.cache, {})
        self.assertIsNone(store.get("first"))
        self.assertIsNone(store.get("second"))


if __name__ == "__main__":
    unittest.main()
