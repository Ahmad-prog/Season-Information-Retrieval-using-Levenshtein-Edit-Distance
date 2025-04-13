# This file defines the data models for our application
# For a simple application, we're using dictionaries, but in a more complex app,
# you might use ORM models like SQLAlchemy

class Drama:
    """
    Represents a Pakistani drama in our database
    """

    def __init__(self, id=None, title=None, director=None, year=None,
                 channel=None, episodes=None, rating=None, description=None,
                 image_path=None):
        self.id = id
        self.title = title
        self.director = director
        self.year = year
        self.channel = channel
        self.episodes = episodes
        self.rating = rating
        self.description = description
        self.image_path = image_path

    def to_dict(self):
        """Convert the Drama object to a dictionary"""
        return {
            'id': self.id,
            'title': self.title,
            'director': self.director,
            'year': self.year,
            'channel': self.channel,
            'episodes': self.episodes,
            'rating': self.rating,
            'description': self.description,
            'image_path': self.image_path
        }

    @classmethod
    def from_dict(cls, data):
        """Create a Drama object from a dictionary"""
        return cls(
            id=data.get('id'),
            title=data.get('title'),
            director=data.get('director'),
            year=data.get('year'),
            channel=data.get('channel'),
            episodes=data.get('episodes'),
            rating=data.get('rating'),
            description=data.get('description'),
            image_path=data.get('image_path')
        )
