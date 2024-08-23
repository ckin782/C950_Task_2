class Truck:
    def __init__(self, id, package_ids, depart_time, distances):
        self.id = id
        self.package_ids = package_ids
        self.mileage = 0
        self.depart_time = depart_time # time truck departs from hub
        self.return_time = None # time truck returns to teh hub
        
        # self.distances: array of distances traveled between each package in package_ids, beginning at the hub and ending at the final package.
        # first element is the distance from the hub to the delivery address of the 1st package.
        # last element is the distance between the delivery addresses of the last two packages delivered.
        self.distances = distances
        