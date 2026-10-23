from store import SessionStore

store = SessionStore()
store.set_user("a")
store.put("first", "private")
store.put("second", 0)
for label in ("logout_once", "logout_twice"):
    store.logout()
    print(label, "user=", repr(store.user), "cache=", repr(store.cache),
          "get_first=", repr(store.get("first")), "get_second=", repr(store.get("second")))
store.set_user("a")
print("same_user_relogin", "user=", repr(store.user), "cache=", repr(store.cache),
      "get_first=", repr(store.get("first")))
