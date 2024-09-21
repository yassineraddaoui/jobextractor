class JobOffer:
    def __init__(self, titre=None, link=None, image=None, company=None, sector=None, location=None, job_type=None, availability=None, description=None, source=None):
        self.titre = titre
        self.link = link
        self.image = image
        self.company = company
        self.sector = sector
        self.location = location
        self.type = job_type  # Renamed to 'job_type' to avoid conflict with Python's built-in 'type'
        self.availability = availability
        self.description = description
        self.source = source

    def to_dict(self):
        return {
            "titre": self.titre,
            "link": self.link,
            "image": self.image,
            "company": self.company,
            "sector": self.sector,
            "location": self.location,
            "type": self.type,
            "availability": self.availability,
            "description": self.description,
            "source": self.source,
        }
