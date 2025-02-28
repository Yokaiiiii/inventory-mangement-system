import pymysql

def get_mysql_user():
    try:
        # Connecting to MySQL
        print("helloworld")
        connection = pymysql.connect(host="localhost", user="learningYokai", password="Le@rning123")
        print("hello world")
        cursor = connection.cursor()

        # Execute the query to get the current user
        cursor.execute("SELECT USER();")
        user = cursor.fetchone()
        print(f"Current MySQL User: {user[0]}")

        cursor.close()
        connection.close()

    except pymysql.MySQLError as e:
        print(f"Error: {e}")

get_mysql_user()
