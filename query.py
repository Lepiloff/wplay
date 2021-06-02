# Events

#TODO add events memebers
def get_event(pk):
    return f"SELECT events.id, events.title, events.creator, events.content, events.status, " \
           f"json_agg(json_build_object('city', locations.city, 'street', locations.street, " \
           f"'building', locations.building, 'lat', locations.lat, 'long', locations.long)) AS location ," \
           f"json_agg(json_build_object('id', activities.id, 'name', activities.name)) AS activity  " \
           f"FROM events  JOIN locations  ON events.location_id=locations.id " \
           f"JOIN activities  ON events.activities_id=activities.id " \
           f"WHERE events.id = {pk} GROUP BY events.id "


get_events = "SELECT json_build_object(" \
        "'id', e.id, 'title', e.title, 'creator', json_agg(c), 'activitie', json_agg(a)," \
        " 'users', jsonb_agg(u), 'location', jsonb_agg(l)) AS events " \
        "FROM events AS e LEFT JOIN event_users AS eu ON e.id = eu.events_id " \
        "LEFT JOIN users AS u ON eu.users_id = u.id " \
        "LEFT JOIN users AS c ON e.creator = c.id " \
        "LEFT JOIN activities AS a ON e.activities_id = a.id " \
        "LEFT JOIN locations AS l ON e.location_id = l.id GROUP BY e.id"


location_create = "INSERT INTO locations(city, street, building, lat, long) " \
                  "VALUES (:city, :street, :house, :lat, :long ) RETURNING id"


event_create = "INSERT INTO events(creator, title, content, location_id, activities_id) " \
               "VALUES (:creator, :title, :content, :location_id, :activities_id) RETURNING id"


event_user_create = "INSERT INTO event_users (events_id, users_id) " \
                    "VALUES (:events_id, :users_id)"


# Activities
create_activity = "INSERT INTO activities(name) VALUES (:name) RETURNING name"


# User profile
def get_profile_info(pk):
        return f"SELECT users.id, users.email, a.user_id as account_id, a.name as name, a.surname as surname, a.personal_info as info " \
               f"FROM users INNER JOIN accounts AS a ON users.id = a.user_id  WHERE users.id = {pk}"

