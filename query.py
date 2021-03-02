# Events

def get_event(_id):
    return f"SELECT json_build_object('id', e.id, 'title', e.title, 'creator', json_agg(c), " \
        f"'activitie', json_agg(a), 'users', jsonb_agg(u), 'location', jsonb_agg(l)) " \
        f"AS event FROM events AS e " \
        f"LEFT JOIN event_users AS eu ON e.id = eu.events_id " \
        f"LEFT JOIN users AS u ON eu.users_id = u.id " \
        f"LEFT JOIN users AS c ON e.creator = c.id " \
        f"LEFT JOIN activities AS a ON e.activities_id = a.id " \
        f"LEFT JOIN locations AS l ON e.location_id = l.id " \
        f"WHERE e.id = {_id} GROUP BY e.id"


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


event_user_create = "INSERT INTO event_users (location_id, activities_id) " \
                    "VALUES (:location_id, :activities_id)"


# Activities

create_activity = "INSERT INTO activities(name) VALUES (:name) RETURNING name"
