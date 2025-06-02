import mysql.connector as mysql
import os
import csv

# class for creation and insertion
class DbUtils:

    def __init__(self, db_connection):
        self.db_connection = db_connection
        self.cursor = db_connection.cursor()


    def create_tables(self):
        """
        Create User, Activity, and TrackPoint tables
        """
        self._create_table_user()
        self._create_table_activity()
        self._create_table_track_point()

    def _create_table_user(self):
        query = """
        CREATE TABLE IF NOT EXISTS User (
            id VARCHAR(30) NOT NULL PRIMARY KEY,
            has_labels BOOL
        );
        """
        self.cursor.execute(query)
        self.db_connection.commit()

    def _create_table_activity(self):
        query = """
        CREATE TABLE IF NOT EXISTS Activity (
            id INT NOT NULL PRIMARY KEY AUTO_INCREMENT,
            user_id VARCHAR(30),
            transportation_mode VARCHAR(255),
            start_date_time DATETIME,
            end_date_time DATETIME,
            FOREIGN KEY(user_id) REFERENCES User(id)
        );
        """
        self.cursor.execute(query)
        self.db_connection.commit()

    def _create_table_track_point(self):
        query = """
        CREATE TABLE IF NOT EXISTS TrackPoint (
            id INT NOT NULL PRIMARY KEY AUTO_INCREMENT,
            activity_id INT,
            lat DOUBLE,
            lon DOUBLE,
            altitude INT,
            date_days DOUBLE,
            date_time DATETIME,
            FOREIGN KEY(activity_id) REFERENCES Activity(id)
        );
        """
        self.cursor.execute(query)
        self.db_connection.commit()

    def insert_user(self, user_id, has_labels):
        """
        Insert a user into the User table.
        """
        query = """
        INSERT INTO User (id, has_labels)
        VALUES (%s, %s)
        ON DUPLICATE KEY UPDATE id=id;
        """
        self.cursor.execute(query, (user_id, has_labels))
        self.db_connection.commit()

    def insert_activity(self, user_id, transportation_mode, start_datetime, end_datetime):
        """
        Insert an activity into the Activity table
        """
        query = """
        INSERT INTO Activity (user_id, transportation_mode, start_date_time, end_date_time)
        VALUES (%s, %s, %s, %s)
        """
        self.cursor.execute(query, (user_id, transportation_mode, start_datetime, end_datetime))
        self.db_connection.commit()
        return self.cursor.lastrowid

    def insert_trackpoints(self, activity_id, trackpoints):
        """
        Batch insert TrackPoints related to an activity.
        """
        query = """
        INSERT INTO TrackPoint (activity_id, lat, lon, altitude, date_days, date_time)
        VALUES (%s, %s, %s, %s, %s, %s)
        """
        self.cursor.executemany(query, trackpoints)
        self.db_connection.commit()

    def close(self):
        self.cursor.close()
        self.db_connection.close()


# Function to read labeled activities
def get_label_match(user_id):
    """
    read label text file for the user and returns a start and finish time
    """
    labels = {}
    label_file_path = f"./dataset/{user_id}/labels.txt"  

    if os.path.exists(label_file_path):
        print(f"Reading labels.txt for user {user_id}...")  
        with open(label_file_path, 'r') as file:
            reader = csv.reader(file, delimiter="\t")
            next(reader)  
            for row in reader:
                start_time = row[0].replace("/", "-")
                end_time = row[1].replace("/", "-")
                transportation_mode = row[2]
                labels[(start_time, end_time)] = transportation_mode
                print(f"Found label: {transportation_mode} from {start_time} to {end_time}")  

    return labels






def process_and_insert_data(db_utils, user_id, labels):
    """
    handles plt files, checks the requirement of less than 2500 trackpoints
    """
    trajectory_dir = f"./dataset/{user_id}/Trajectory/"

    # Check if the Trajectory file exists for the user
    if not os.path.exists(trajectory_dir):
        print(f"Trajectory directory not found for user {user_id}.")
        return

    print(f"Looking for .plt files in {trajectory_dir}...")  

    # Iterates through the plt files
    for file_name in os.listdir(trajectory_dir):
        if file_name.endswith(".plt"):  
            print(f"Processing file {file_name} for user {user_id}...") 

            file_path = os.path.join(trajectory_dir, file_name)

            trackpoints = []
            with open(file_path, 'r') as file:
                reader = csv.reader(file)
                for i, row in enumerate(reader):
                    if i < 6:  # Skips the header
                        continue
                    trackpoints.append((
                        float(row[0]),  # lat
                        float(row[1]),  # lon
                        float(row[3]),    # altitude
                        float(row[4]),  # date_days
                        f"{row[5]} {row[6]}"  # date_time (Combination of date and time)
                    ))

            #Checks requirement of less 2500
            if len(trackpoints) <= 2500:
                print(f"Inserting activity for {len(trackpoints)} trackpoints for user {user_id}...") 

                start_datetime_str = trackpoints[0][-1]
                end_datetime_str = trackpoints[-1][-1]

                # Finds match for transportation mode
                transportation_mode = labels.get((start_datetime_str, end_datetime_str), None)

                # Inserts activity to transportation mode
                activity_id = db_utils.insert_activity(user_id, transportation_mode, start_datetime_str, end_datetime_str)

                # Inserts TracksPoints in batches, 500 at the time(largoe amount)
                batch_size = 500
                for i in range(0, len(trackpoints), batch_size):
                    batch = trackpoints[i:i + batch_size]
                    db_utils.insert_trackpoints(activity_id, [(activity_id, *tp) for tp in batch])

                print(f"Inserted activity for user {user_id} with {len(trackpoints)} trackpoints and transportation mode '{transportation_mode}'.")
            else:
                print(f"Skipped activity in {file_name} for user {user_id} exceeding 2500 trackpoints.")





