from PackageStatus import PackageStatus

class Package:
    def __init__(self, id, address, city, state, zipcode, deadline, weight, notes):
        # depart_time, arrive_time are time objects
        self.depart_time = None
        self.delivery_time = None
        
        self.id = id
        self.address = address
        self.city = city
        self.state = state
        self.zipcode = zipcode
        self.deadline = deadline
        self.weight = weight
        self.notes = notes
        self.truck_id = None
        
        # I created an Enum class, PackageStatus, such that status can only have 3 possible values (c.f. PackageStatus). 
        # Every package begins at the hub by default.
        self.status = PackageStatus.AT_HUB
