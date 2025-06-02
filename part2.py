from DbConnector import DbConnector
from tabulate import tabulate
from geopy.distance import geodesic

class Part2:
    def __init__(self, db_connection):
        """
        Initialize part2 class
        """
        self.db_connection = db_connection
        self.cursor = self.db_connection.cursor()

    def task1(self):
        print("\n_________TASK 1_________")

        # collect results in an array
        results = []

        # Query to count users
        self.cursor.execute("SELECT COUNT(*) FROM User")
        user_count = self.cursor.fetchone()[0]  
        results.append(("User Count", user_count))  # add to array

        # Query to count activity
        self.cursor.execute("SELECT COUNT(*) FROM Activity")
        activity_count = self.cursor.fetchone()[0]  
        results.append(("Activity Count", activity_count))  

        # Query to count trackpoints
        self.cursor.execute("SELECT COUNT(*) FROM TrackPoint")
        trackpoint_count = self.cursor.fetchone()[0]  
        results.append(("TrackPoint Count", trackpoint_count))  



        print(tabulate(results, headers=["Type", "Count"], tablefmt="fancy_grid"))

    def task2(self):
        print("\n_________TASK 2_________")

        # SQL-query to find average activities per user
        query = """
            SELECT AVG(activities_per_User) 
            FROM (
                SELECT COUNT(*) as activities_per_User
                FROM Activity
                GROUP BY Activity.user_id
            ) as counts
        """
        self.cursor.execute(query)
        avg_activities_per_user = self.cursor.fetchone()[0]  # get the result from the query

        # Displays the result in a pretty table
        results = [("Average Activities Per User", avg_activities_per_user)]
        print(f"Average Activities Per User: {avg_activities_per_user:.2f}")


    def task3(self):
        print("\n_________TASK 3_________")

        # SQL query for finding the top 20 users
        query = """
                SELECT user_id, COUNT(*) as top_20_count
                FROM Activity
                GROUP BY Activity.user_id
                ORDER BY top_20_count DESC
                LIMIT 20
        """
        self.cursor.execute(query)
        rows = self.cursor.fetchall()  

        # results in a list of tuples)
        results = [(row[0], row[1]) for row in rows]                 
    
    
        print(tabulate(results, headers=["User ID", "Activity Count"], tablefmt="fancy_grid"))

    def task4(self):
        print("\n_________TASK 4: Find all users who have taken a taxi_________")

        # SQL-query to find users who has taken a taxi
        query = """
                SELECT DISTINCT user_id
                FROM Activity
                WHERE transportation_mode = 'taxi'
        """
        self.cursor.execute(query)
        rows = self.cursor.fetchall()  


        results = [(row[0],) for row in rows]  


        self.print_table(results)
    
    def print_table(self, results):
        """
        writes result in a table.
        """
        print(tabulate(results, headers=["User ID"], tablefmt="fancy_grid"))

    def task5(self):
        print("\n_________TASK 5: Transportation modes and activity count_________")
        
        # SQL-queries who counts activities, except NULL 
        query = """
                SELECT transportation_mode, COUNT(*) as activity_count
                FROM Activity
                WHERE transportation_mode IS NOT NULL
                GROUP BY transportation_mode;
        """
        
        self.cursor.execute(query)
        
        rows = self.cursor.fetchall()
        
        print(tabulate(rows, headers=["Transportation Mode", "Count"], tablefmt="fancy_grid"))


    def task6a(self):
        print("\n_________TASK 6a: Year with the most activities_________")
        
        # SQL-queri that finds the year with the most activities
        query = """
            SELECT YEAR(start_date_time) as year, COUNT(*) as activity_count
            FROM Activity
            GROUP BY year
            ORDER BY activity_count DESC
            LIMIT 1;
        """
        
        self.cursor.execute(query)
        
        result = self.cursor.fetchone()
        
        if result:
            print(f"The year with the most activities is {result[0]} with {result[1]} activities.")
        else:
            print("No activities found.")
    
    def task6b(self):
        print("\n_________TASK 6b: Year with the most recorded hours_________")
        
        # SQL-quiery that finds the year with the most hours
        query = """
            SELECT YEAR(start_date_time) as year, SUM(TIMESTAMPDIFF(HOUR, start_date_time, end_date_time)) as total_hours
            FROM Activity
            GROUP BY year
            ORDER BY total_hours DESC
            LIMIT 1;
        """
        
        self.cursor.execute(query)
        
        
        result = self.cursor.fetchone()
        
        if result:
            print(f"The year with the most recorded hours is {result[0]} with {result[1]} hours.")
        else:
            print("No activities found.")

    
    def task7(self):
        print("\n_________TASK 7: Total Distance Walked in 2008 by User 112_________")
        query = """
        SELECT TrackPoint.lat, TrackPoint.lon
        FROM TrackPoint
        JOIN Activity ON Activity.id = TrackPoint.activity_id
        WHERE Activity.user_id = '112' AND YEAR(Activity.start_date_time) = 2008 AND Activity.transportation_mode = 'walk'
        ORDER BY Activity.id, TrackPoint.date_time;
        """
        
        self.cursor.execute(query)
        rows = self.cursor.fetchall()

        #Calculates the total distamce by iterating using geopy
        total_distance = 0
        if rows:
            previous_point = None
            for point in rows:
                current_point = (point[0], point[1])
                if previous_point is not None:
                    total_distance += geodesic(previous_point, current_point).kilometers
                previous_point = current_point

        print(f"Total Distance Walked (km): {total_distance:.2f}")
    
    def task8(self):
        print("\n_________TASK 8: Total altitude gained by users_________")
        
        # SQL-quiery calculates total altitude for users
        query = """
            SELECT user_id, SUM(altitude_diff) as total_altitude_gained
            FROM (
                SELECT A.user_id, 
                    (T.altitude - LAG(T.altitude) OVER(PARTITION BY T.activity_id ORDER BY T.id)) as altitude_diff
                FROM TrackPoint T
                LEFT JOIN Activity A ON A.id = T.activity_id
                WHERE T.altitude != -777  -- Ekskluder ugyldige høyder
            ) AS altitude_difference
            WHERE altitude_diff > 0  -- Beregn kun oppovergående høydeforskjeller
            GROUP BY user_id
            ORDER BY total_altitude_gained DESC
            LIMIT 20;
        """
        
        
        self.cursor.execute(query)
        
        
        rows = self.cursor.fetchall()
        
        
        if rows:
            print(f"Top 20 users by total altitude gained:")
            print(tabulate(rows, headers=["User ID", "Total Altitude Gained (m)"], tablefmt="fancy_grid"))
        else:
            print("No altitude data found.")

    def task9(self):
        print("\n_________TASK 9: Users with invalid activities_________")
        
        # SQL-quiery that finds invalid activties
        query = """
            SELECT user_id, COUNT(DISTINCT activity_id) AS invalid_activity_count
            FROM (
                SELECT A.user_id, A.id AS activity_id, 
                    TIMESTAMPDIFF(MINUTE, LAG(T.date_time) OVER (PARTITION BY T.activity_id ORDER BY T.id), T.date_time) AS time_diff
                FROM TrackPoint T
                JOIN Activity A ON A.id = T.activity_id
            ) AS time_differences
            WHERE time_diff >= 5
            GROUP BY user_id
            ORDER BY invalid_activity_count DESC;
        """
        
        
        self.cursor.execute(query)
        
        
        rows = self.cursor.fetchall()
        
        
        if rows:
            print(f"Users with invalid activities and the count of invalid activities:")
            print(tabulate(rows, headers=["User ID", "Invalid Activity Count"], tablefmt="fancy_grid"))
        else:
            print("No invalid activities found.")

    def task10(self):
        print("\n_________TASK 10: Users with activities in the Forbidden City_________")
        
        # SQL-quieri that finds users who has done activites in the forbidden city
        query = """
            SELECT DISTINCT A.user_id
            FROM TrackPoint T
            JOIN Activity A ON T.activity_id = A.id
            WHERE T.lat BETWEEN 39.915 AND 39.917  -- latituden 39.916
            AND T.lon BETWEEN 116.396 AND 116.398  -- longituden 116.397;
        """
        
        
        self.cursor.execute(query)
        
        
        rows = self.cursor.fetchall()
        
        
        if rows:
            print(f"Users who have tracked an activity in the Forbidden City:")
            print(tabulate(rows, headers=["User ID"], tablefmt="fancy_grid"))
        else:
            print("No users found with activities in the Forbidden City.")


    def task11(self):
        print("\n_________TASK 11: Most used transportation mode per user_________")
        
        # SQL-quieri that finds the most frequent used transporationmode to a user
        query = """
            SELECT user_id, transportation_mode
            FROM (
                SELECT A.user_id, A.transportation_mode, 
                    ROW_NUMBER() OVER (PARTITION BY A.user_id ORDER BY COUNT(*) DESC) as rn
                FROM Activity A
                WHERE A.transportation_mode IS NOT NULL
                GROUP BY A.user_id, A.transportation_mode
            ) AS ranked_modes
            WHERE rn = 1
            ORDER BY user_id;
        """
        
        
        self.cursor.execute(query)
        
        
        rows = self.cursor.fetchall()
        
        # Writes the result in a pretty table
        if rows:
            print(f"Users and their most used transportation mode:")
            print(tabulate(rows, headers=["User ID", "Most Used Transportation Mode"], tablefmt="fancy_grid"))
        else:
            print("No users found with transportation modes.")

        
