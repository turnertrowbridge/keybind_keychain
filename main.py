import database

def main():
    db = database.Database("applications.db", database.DatabaseType.Applications)


if __name__ == "__main__":
    main()