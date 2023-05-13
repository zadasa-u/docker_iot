import environs

env = environs.Env(eager=False)
env.read_env()  # read .env file, if it exists


class Config:
    MARIADB_USER = env.str("MARIADB_USER")
    MARIADB_USER_PASS = env.str("MARIADB_USER_PASS")
    MARIADB_DB = env.str("MARIADB_DB")
    MARIADB_SERVER = env.str("MARIADB_SERVER")
    PUERTO = env.int("PUERTO")
    LOG_LEVEL = env.str("LOG_LEVEL").upper()
    MARIADB_DB_TABLES_LIST = env.list("MARIADB_DB_TABLES_LIST")


env.seal()
