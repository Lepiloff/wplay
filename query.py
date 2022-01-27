# TODO remove f-string

# Events

#TODO add events memebers

get_event = """
    SELECT
        events.id, events.title, events.creator, events.content, events.status,
        (json_agg(json_build_object('city', locations.city, 'street', locations.street,
        'building', locations.building, 'lat', locations.lat, 'long', locations.long)) -> 0)AS location,
        (json_agg(json_build_object('id', activities.id, 'name', activities.name)) -> 0) AS activity,
        (json_agg(json_build_object('name', accounts.name, 'surname', accounts.surname)) -> 0) AS creator
    FROM
        events
    JOIN
        locations ON events.location_id=locations.id
    JOIN
        activities ON events.activities_id=activities.id
    JOIN
        accounts ON events.creator=accounts.user_id
    WHERE events.id = :pk GROUP BY events.id
"""


get_events = """
    SELECT 
        events.id, events.title, events.content, events.status, 
        (json_agg(json_build_object('city', locations.city, 'street', locations.street,
        'building', locations.building, 'lat', locations.lat, 'long', locations.long)) -> 0)AS location ,
        (json_agg(json_build_object('id', activities.id, 'name', activities.name)) -> 0) AS activity,
        (json_agg(json_build_object('name', accounts.name, 'surname', accounts.surname)) -> 0) AS creator
    FROM 
        events  
    JOIN 
        locations  ON events.location_id=locations.id
    JOIN 
        activities  ON events.activities_id=activities.id
    JOIN
        accounts ON events.creator=accounts.user_id
    GROUP BY events.id
"""


event_create = "INSERT INTO events(creator, title, content, location_id, activities_id, start_date, start_time, is_private) " \
               "VALUES (:creator, :title, :content, :location_id, :activities_id, :start_date, :start_time, :is_private) RETURNING id"


event_user_create = "INSERT INTO event_users (events_id, users_id) " \
                    "VALUES (:events_id, :users_id)"
# Location
location_create = "INSERT INTO locations(country, city, street, building, lat, long) " \
                  "VALUES (:country, :city, :street, :house, :lat, :long ) RETURNING id"


# Activities
create_activity = "INSERT INTO activities(name) VALUES (:name) RETURNING name"

# User profile
get_profile_info = "SELECT users.id, users.email, a.user_id as account_id, a.name as name, a.surname as surname, a.personal_info as info " \
                   "FROM users INNER JOIN accounts AS a ON users.id = a.user_id  WHERE users.id = :pk"

# Notifications
get_user_notifications = "SELECT * FROM notifications WHERE user = :user"

# Messages
get_message_count = "SELECT COUNT(*) AS TOTAL, " \
        "(SELECT COUNT(*) FROM messages WHERE type='FRIENDSHIP' AND messages.recipient = :user_id AND messages.is_read is False) AS friends, " \
        "(SELECT COUNT(*) FROM messages WHERE type='EVENT' AND messages.recipient = :user_id  AND messages.is_read is False) AS events " \
        "FROM messages WHERE messages.recipient = :user_id GROUP BY messages.recipient"



