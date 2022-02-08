import api.lib.db as db
from api.lib.orm import build_from_record
import api.models as models

class Venue:
    columns = ['id', 'foursquare_id', 'name', 'price',
            'rating', 'likes', 'menu_url']
    __table__ = 'venues'
    
    def __init__(self, **kwargs):
        for key in kwargs.keys():
            if key not in self.columns:
                raise f'{key} not in {self.columns}' 
        for k, v in kwargs.items():
            setattr(self, k, v)

    @classmethod
    def find_by_foursquare_id(self, foursquare_id, conn):
        cursor = conn.cursor()
        cursor.execute('SELECT * from venues where foursquare_id = %s', (foursquare_id,))
        record = cursor.fetchone()
        if not record: 
            return None
        else:
            return build_from_record(Venue, record)

    # added
    def categories(self, cursor):
        venues_query = """SELECT categories.* FROM categories
        JOIN venue_categories ON
        venue_categories.category_id = categories.id 
        WHERE venue_categories.venue_id = %s"""
        cursor.execute(venues_query, (self.id,))
        venue_records = cursor.fetchall()
        return [build_from_record(models.Category, record) 
        for record in venue_records]

    def to_json(self, cursor):
        attr = self.__dict__
        category_names = [category.name for category in self.categories(cursor)]
        attr_list = list(attr.items())
        attr_list.append(('categories', category_names))
        return dict(attr_list)
        
