import unittest

from store import SessionStore


class AcceptanceRound2(unittest.TestCase):
    def test_A_instances_start_empty_and_are_independent(self):
        first = SessionStore()
        second = SessionStore()
        for store in (first, second):
            self.assertIsNone(store.user)
            self.assertEqual(store.cache, {})
        first.set_user("a")
        first.put("private", 1)
        self.assertIsNone(second.user)
        self.assertEqual(second.cache, {})

    def test_B_identity_transitions_preserve_or_clear_every_entry(self):
        store = SessionStore()
        for previous, current in ((None, "a"), ("a", "a"), ("a", "b"),
                                  ("b", "a"), ("a", None), (None, None)):
            with self.subTest(previous=previous, current=current):
                self.assertEqual(store.user, previous)
                store.put("one", 0)
                store.put("two", False)
                store.set_user(current)
                self.assertEqual(store.user, current)
                expected = {"one": 0, "two": False} if previous == current else {}
                self.assertEqual(store.cache, expected)
                for key in ("one", "two"):
                    self.assertEqual(store.get(key), expected.get(key))

    def test_C_writes_overwrite_and_missing_reads_do_not_mutate(self):
        store = SessionStore()
        store.set_user("a")
        values = ("value", 0, False, "", None, [], {"nested": True})
        for value in values:
            with self.subTest(value=value):
                store.put("key", value)
                self.assertIs(store.get("key"), value)
                self.assertEqual(len(store.cache), 1)
                self.assertIsNone(store.get("absent"))
                self.assertEqual(len(store.cache), 1)

    def test_D_logout_clears_immediately_and_is_repeatable(self):
        for user in (None, "a"):
            for populated in (False, True):
                with self.subTest(user=user, populated=populated):
                    store = SessionStore()
                    store.set_user(user)
                    if populated:
                        store.put("one", "private")
                        store.put("two", 0)
                    for _ in range(3):
                        store.logout()
                        self.assertIsNone(store.user)
                        self.assertEqual(store.cache, {})
                        self.assertIsNone(store.get("one"))
                        self.assertIsNone(store.get("two"))

    def test_E_repeated_relogin_cycles_never_restore_old_values(self):
        store = SessionStore()
        for user in ("a", "a", "b", "a"):
            store.set_user(user)
            self.assertEqual(store.user, user)
            self.assertEqual(store.cache, {})
            self.assertIsNone(store.get("private"))
            store.put("private", user)
            store.logout()
            self.assertIsNone(store.user)
            self.assertIsNone(store.get("private"))


if __name__ == "__main__":
    unittest.main()
