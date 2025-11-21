"""Project package initializer.

If mysqlclient (MySQLdb) is not available at runtime, attempt to use PyMySQL
as a drop-in replacement by calling pymysql.install_as_MySQLdb(). This makes
it easier to run the project in environments where compiling mysqlclient is
not possible. If you prefer to use the native mysqlclient, install it and
PyMySQL fallback won't be necessary.
"""
try:
    # Try to import the native MySQLdb (provided by mysqlclient)
    import MySQLdb  # type: ignore
except Exception:
    try:
        import pymysql

        pymysql.install_as_MySQLdb()
    except Exception:
        # Neither mysqlclient nor PyMySQL available — that's fine for sqlite default.
        pass
