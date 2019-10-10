import shelve

class database:
    """
    This is the class used to access the database.
    """

    @staticmethod
    def add(key, value):
        with shelve.open(filename="database", flag="c", writeback = True) as db:
            db[key] = value

    @staticmethod
    def delete(key):
        with shelve.open(filename="database", flag="w", writeback = True) as db:
            del db[key]

    @staticmethod
    def access(key):
        with shelve.open(filename="database", flag="r", writeback = False) as db:
            return db[key]

    @staticmethod
    def has(key):
        with shelve.open(filename="database", flag="r", writeback = False) as db:
            db.has_key(key)