def get_location(id):
    from db import Location
    l = Location.query.filter_by(id=id)
    if l.count() > 0:
        return l.first()
    return None

def add_location(longitude, latitude):
    from db import Location, db
    
    location = Location()
    location.longitude = longitude
    location.latitude = latitude
    
    db.session.add(location)
    db.session.commit()
    
    return location