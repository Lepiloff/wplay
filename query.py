# TODO remove f-string

# Events

get_event = """
SELECT
    e.id, e.title, e.creator, e.content, e.status, e.start_date, e.start_time,
    (json_agg(json_build_object('city', locations.city, 'street', locations.street,
    'building', locations.building, 'lat', locations.lat, 'long', locations.long)) -> 0) AS location,
    (json_agg(json_build_object('id', activities.id, 'name', activities.name)) -> 0) AS activity,
    (json_agg(json_build_object('name', a.name, 'surname', a.surname)) -> 0) AS creator_info,
    case when count(m.user_id) = 0 then '[]' 
    else json_agg(json_build_object('id', m.user_id, 'name', m.name, 'surname', m.surname)) end members
FROM
    events AS e
INNER JOIN
    locations ON e.location_id=locations.id
INNER JOIN
    activities ON e.activities_id=activities.id
INNER JOIN 
    accounts AS a ON  e.creator=a.user_id
LEFT JOIN (
  SELECT events_id AS id, 
          a.user_id,
          a.name,
          a.surname
  FROM event_users AS e
  INNER JOIN accounts AS a ON a.user_id = e.users_id
) m ON m.id = e.id
WHERE e.id = :pk 
GROUP BY e.id, e.title, e.creator, e.content, e.status
"""

get_events = """
SELECT 
    e.id, e.title, e.status, e.start_date, e.start_time,
    (json_agg(json_build_object('lat', locations.lat, 'long', locations.long)) -> 0)AS location ,
    (json_agg(json_build_object('id', activities.id, 'name', activities.name)) -> 0) AS activity
FROM 
    events AS e
JOIN 
    locations  ON e.location_id=locations.id
JOIN 
    activities  ON e.activities_id=activities.id
GROUP BY e.id
"""


event_create = "INSERT INTO events(creator, title, content, location_id, activities_id, start_date, start_time, members_count, is_private) " \
               "VALUES (:creator, :title, :content, :location_id, :activities_id, :start_date, :start_time, :members_count, :is_private) RETURNING id"


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

