class University:
    def __init__(self, name, faundation_date, location, small_info):
        self.name = name
        self.faundation_date = faundation_date
        self.location = location
        self.small_info = small_info

def init_universities_db(cursor):
    query = """DROP TABLE IF EXIST UNIVERSITIES"""
    cursor.execute(query)
    query = """CREATE TABLE UNIVERSITIES (
        NAME varchar(100) NOT NULL,
        FAUNDATION_DATE integer NOT NULL,
        LOCATION varchar(80) NOT NULL,
        SMALL_INFO varchar(500),
        PRIMARY KEY (NAME, FAUNDATION_DATE, LOCATION
        )"""
    cursor.execute(query)

def add_university(cursor, request, variables):
    query = """INSERT INTO FIXTURE
        (NAME, FAUNDATION_DATE, LOCATION, SMALL_INFO) VALUES (
        %s,
        %d,
        %s,
        %s
        )"""
    cursor.execute(query, variables)