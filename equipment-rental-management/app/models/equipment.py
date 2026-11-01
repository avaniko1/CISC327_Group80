class Equipment:
    def __init__(self, id, name, category, total_units, available_units, out_of_service_units=0, is_damaged_units=0, is_available=True, is_damaged=False):
        self.id = id
        self.name = name
        self.category = category
        self.total_units = total_units
        self.available_units = available_units
        self.is_available = is_available  # False when out-of-service / under repair
        self.out_of_service_units= out_of_service_units
        self.is_damaged_units = is_damaged_units
        self.is_damaged=is_damaged

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "category": self.category,
            "total_units": self.total_units,
            "available_units": self.available_units,
            "is_available": self.is_available,
            "out_of_service_units": self.out_of_service_units,
            "is_damaged_units": self.is_damaged_units,
            "is_damaged":self.is_damaged,
        }
