# Student ID: 011999412


import csv

from Truck import Truck
from Package import Package
from PackageStatus import PackageStatus
from HashTable import PackageHashTable

from datetime import timedelta, datetime, time


# truck delivery speed is a given constant
TRUCK_SPEED = 18.0

# initialize package hashtable
package_hashtable = PackageHashTable()

# initialize trucks with temporary values
truck_1 = None
truck_2 = None
truck_3 = None

# initalize 2D array of distances (provided by instructors)
distances = [] 
with open("distances.csv") as distances_csv:
    reader = csv.reader(distances_csv)
    distances = [row for row in reader]


def package_az(id):
    """
    Returns address + ' ' + zipcode for id package
    """
    package = package_hashtable.get(id)
    address = package.address
    zipcode = package.zipcode
    
    addrzip = address + ' (' + zipcode + ')'
    return addrzip


def to_la(az):
    """
    # converts an address with a zipcode (az) to its corresponding long address (la)
    """
    num_rows = len(distances)
    for i in range(1, num_rows):
        row = distances[i]
        row_az = row[1]
        
        if row_az == az:
            row_la = row[0]
            return row_la
        
def row_idx(la):
    """
    returns the index of the row containing the given long address in distances
    """
    num_rows = len(distances)
    for i in range(1, num_rows): # start at 2nd row b/c 1st row is just column names
        row = distances[i]
        row_la = row[0]
        if row_la == la:
            return i

def col_idx(la):
    """
    returns the index of the column containing the given long address in distances
    """
    row0 = distances[0] # first row
    num_cols = len(row0)
    for i in range(2, num_cols):
        col_la = row0[i]
        if col_la == la:
            return i
        

def dist_az(az1, az2):    
    """
    Returns the distance between two addresses with zipcodes.
    
    Args:
        az1, az2 -- address with zipcode 1,2
        distances: distances.csv as 2d list
    
    Returns:
        outputs: distance between them
    """
    # convert az1, az2 to la's (i.e. to long addresses in distances.csv)

    la1 = to_la(az1)
    la2 = to_la(az2)
    
    # get the row and column indecies
    r_idx = row_idx(la1)
    c_idx = col_idx(la2)
    
    # because the distances table is lower-triangular, we can't access any (r_idx, c_idx) in the top right triangle. If our (r_idx, c_idx) is in the top right triangle, we have to flip them.
    if (r_idx - 1) < (c_idx - 2):
        temp = r_idx
        r_idx = c_idx-1
        c_idx = temp+1
    
    # find distance between these two la's
    d12_str = distances[r_idx][c_idx]
    d12 = float(d12_str)
    
    # return distance
    return d12


def dist_between_package_ids(id1, id2):
    """
    Returns the distance between the addresses of two packages with id's of id1 and id2, respectively.
    """
    # get the address-with-zipcode of both packages
    az1 = package_az(id1)
    az2 = package_az(id2)
    
    d12_str = dist_az(az1, az2)
    dist12 = float(d12_str)
    
    
    return dist12

    
def nearest_neighbor_order(ids):
    """
    Sorts the given list of package ids using a nearest neighbor algorithm. 
    Returns a list containing 2 lists: 
    1) list of package ids in order that they'll be delievered, determined by nearest neighbor algorithm;
    2) list of distances between each package (in the order chosen by the NN alg.)
    
    Args: 
        ids: list of package ids
        distances: lower-triangular matrix of distances between addresses
    """
    initial_address = "4001 South 700 East, Salt Lake City, UT 84107" # all trucks start here
    cur_az = initial_address # current address with zipcode
    unsorted_ids = ids
    sorted_ids = []
    distances = []
    
    for x in range(len(unsorted_ids)):
        min_id = unsorted_ids[0]
        min_dist = dist_az(cur_az, package_az(min_id)) # distance between current address and the first address in unsorted_ids
        for id in unsorted_ids:
            az2 = package_az(id)
            d = dist_az(cur_az, az2)
            if d < min_dist:
                min_id = id
                min_dist = d
        distances.append(min_dist)
        unsorted_ids.remove(min_id)
        sorted_ids.append(min_id)
        cur_az = package_az(min_id)
        
    return [sorted_ids, distances]


def increase_time(old_time: time, hours: float) -> time:
    """
    Increases a given time by a specified number of hours.

    Args:
        old_time (time): The starting time.
        hours (float): The number of hours to add. Can be a floating-point number.

    Returns:
        time: A new time object representing old_time + hours.
    """
    # Convert old_time to datetime
    dt = datetime.combine(datetime.min, old_time)
    
    # Create timedelta from hours and add to datetime
    new_dt = dt + timedelta(hours=hours)
    
    # Extract and return the new time
    return new_dt.time()


def deliver_truck(truck):
    """
    Deliver all of the packages on a truck. 
    
    Args:
        truck: Truck object. The Truck whose packages are delievered.
    """
    # list of package ids in the order that we are going to deliver them.
    package_ids = truck.package_ids 
    # the current time, for the truck
    current_time = truck.depart_time
    
    # the address of the hub (the truck departs from here, and finally returns here after delivering all of its packages.)
    hub_address = "4001 South 700 East, Salt Lake City, UT 84107"
    # the last package we delievered
    previous_package = None 
    # the package we are going to deliver next
    next_package = None
    # distance to the next package
    next_distance = 0.0
    # total distance we have traveled so far
    total_distance = 0.0
    
    # True when we have not delievered the package with the first package_id in package_ids; False afterwards.
    first_id = True

    # All package deliveries are reflected in changes to package_hashtable
    for package_id in package_ids:
        next_package = package_hashtable.get(package_id)
        next_package.depart_time = current_time
        
        if first_id:
            next_distance = dist_az(hub_address, package_az(package_id))
            first_id = False
        else:
            next_distance = dist_between_package_ids(previous_package.id, next_package.id)
            
        # next_hours: time in hours it is going to take to travel from the current address to the address of the next package (i.e. its delivery address)
        next_hours = next_distance/TRUCK_SPEED
        
        # deliver the package and update local variables, package, and truck accordingly
        current_time = increase_time(current_time, next_hours)
        
        total_distance += next_distance
        
        next_package.delivery_time = current_time
        next_package.status = PackageStatus.DELIVERED        
        
        package_hashtable.insert(package_id, next_package)
        previous_package = next_package
        
    # all packages delivered. Truck now must drive back to the hub.
    next_distance = dist_az(package_az(previous_package.id), hub_address)
    next_hours = next_distance/TRUCK_SPEED
    current_time = increase_time(current_time, next_hours)
    total_distance += next_distance
    truck.mileage = total_distance
    truck.return_time = current_time


    

def set_truck_id(package_ids, truck_id):
    """
    Sets the truck_id variable of all of the packages in package_hashtable with the given package_id's to the given truck_id
    """
    for package_id in package_ids:
        package = package_hashtable.get(package_id)
        package.truck_id = truck_id
        package_hashtable.insert(package_id, package)

def deliver_all():
    """
    Delivers all of the packages, using 3 trucks and 2 drivers, in a way that complies with the notes provided for each package.
    """
    # extract package data from packages.csv, put into packages
    packages = [] # holds all 40 packages (id 1 to 40)
    with open("packages.csv") as packages_csv:
        reader = csv.reader(packages_csv)
        in_header_row = True
        for row in reader:
            if in_header_row:
                in_header_row = False
            else:
                # note: id is initially a char like '1'. I convert it to an integer using int(id)
                id, address, city, state, zipcode, deadline, weight, notes = int(row[0]), row[1], row[2], row[3], row[4], row[5], row[6], row[7]
                package = Package(id, address, city, state, zipcode, deadline, weight, notes)
                packages.append(package)
                package_hashtable.insert(id, package)
        
    # load packages to truck. the order in which they are to be delievered, for each truck, is determined by a nearest neighbor algorithm, and the order of the package ids placed into each truck is that order.
    package_ids_1 = [14,15,16,19,20,34,25,21,22,23,24,26,7,11,32,4]
    package_ids_2 = [1,13,6,29,30,31,37,40,27,35,2,3,18,36,38,5]
    package_ids_3 = [8,9,10,12,17,28,33,39]

    ordered_package_ids_1, distances_1 = nearest_neighbor_order(package_ids_1)
    ordered_package_ids_2, distances_2 = nearest_neighbor_order(package_ids_2)
    ordered_package_ids_3, distances_3 = nearest_neighbor_order(package_ids_3)
        
    # set first depart times for trucks 1, 2
    depart_time_12 = time(hour=9, minute=5, second=0) # 9:05 am
    
    global truck_1
    global truck_2
    global truck_3
    
    # create, load trucks
    truck_1 = Truck(1, ordered_package_ids_1, depart_time_12, distances_1)
    truck_2 = Truck(2, ordered_package_ids_2, depart_time_12, distances_2)
    
    # set truck_id of all packages
    set_truck_id(ordered_package_ids_1, 1)
    set_truck_id(ordered_package_ids_2, 2)
    set_truck_id(ordered_package_ids_3, 3)
    
    # deliver all of the packages
    # we start with the first two trucks, because the truck that delivers the third subset of the packages depends on which of the two trucks finishes its route first
    deliver_truck(truck_1)
    deliver_truck(truck_2)
    
    # since there's only 2 drivers, truck_3 can only depart when one of the 2 first trucks (truck_1, truck_2) returns to the hub. whichever of those trucks returns first, the driver exits that truck and gets into truck_3
    depart_time_3 = None
    if truck_1.return_time < truck_2.return_time:
        depart_time_3 = truck_1.return_time
    else:
        depart_time_3 = truck_2.return_time
        
    truck_3 = Truck(3, ordered_package_ids_3, depart_time_3, distances_3)
    
    deliver_truck(truck_3)
    
    
def get_package_status(id, the_time):
    """
    Returns the status of the package with the given id at the given time.
    
    Args:
        id: id of the package
        time: time for which the package status is returned
    
    Returns:
        String containing the status of the package at the given time.
    """
    package = package_hashtable.get(id)
    truck_id = package.truck_id
    truck = None
    if truck_id == 1:
        truck = truck_1
    elif truck_id == 2:
        truck = truck_2
    else:
        truck = truck_3
    
    truck_depart_time = truck.depart_time
    truck_return_time = truck.return_time
    
    # index of the package in the truck's package_ids. computed below.
    index_of_package = 0
    for id in truck.package_ids:
        if package.id == id:
            break
        index_of_package += 1
    
    # number of miles that the truck travels before delivering the package. computed below.
    distance_before_delivery = 0.00
    for i in range(index_of_package):
        distance_before_delivery += truck.distances[i]
        
    
    hours_before_delivery = distance_before_delivery/TRUCK_SPEED
    # compute package delivery time using truck departure time + the amount of time elapsed before the package is delivered.
    
    package_delivery_time = increase_time(truck_depart_time, hours_before_delivery)
    
    if the_time < truck_depart_time: # truck has not yet left the hub
        return PackageStatus.AT_HUB
    elif the_time < package_delivery_time:
        return PackageStatus.EN_ROUTE
    else:
        return PackageStatus.DELIVERED
    
    

def hours_between(time1: time, time2: time) -> float:
    """
    Calculates the floating-point number of hours between the 2 given time objects.

    If time2 is later than time1, returns 0.

    Args:
        time1 (time): The starting time (must be earlier than time2).
        time2 (time): The ending time (must be later than time1).

    Returns:
        float: The number of hours between time1 and time2, as a floating-point number.
    """
    # If time2 is later than time1, returns 0.
    if time2 <= time1:
        return 0.0
    
    # Convert both times to minutes since midnight
    hours1 = time1.hour + (time1.minute / 60.0)
    hours2 = time2.hour + (time2.minute / 60.0)
    
    # Calculate the difference
    hours_diff = hours2 - hours1
    
    return hours_diff
    

def user_interface():
    """
    User interface. User can input a time and a package id, and get 
    the package status at that time, the mileages of the trucks at that time, and the package delivery time.
    """
    # necessary to compute truck departure times
    deliver_all()     

    # determine whether a user wants to see the status of specfic package, or all packages
        
    choice = ''    
    package_ids = None

    # User indicates whether they want to see the status fo all, or one, package. If they want one package, we have the user input a specific package id.
    # Package_ids will hold either the specific package id given by the user (for choice = 1), or the id of every single package (for choice = 0).
    choice_made = False
    while not choice_made:
        choice = input("Input 0 if you'd like to see the status of all packages, or input 1 if you want to see the status of a specific package: ")
        
        if (choice == '0'): # all packages
            choice_made = True
            package_ids = package_hashtable.get_ids()
            
        elif (choice == '1'):
            choice_made = True
            # Get user inputs
            package_id = None
            current_time = None
        
            # get package id
            package_id_given = False
            while not package_id_given:
                package_id = input("Please input the package id: ")
                try:
                    package_id = int(package_id)
                except ValueError:
                    print("You did not input a valid package id. Please try again.")
                valid_package_ids = package_hashtable.get_ids()
                
                for valid_id in valid_package_ids:
                    if int(package_id) == int(valid_id):
                        package_id_given = True # user input a valid package id
                
                if not package_id_given:
                    print("You did not input a valid package id. Please try again.")
                else:
                    package_ids = [package_id]
            
        else:
            choiceMade = False
            print("You did not input a 0 or a 1. Please try again.")
    
    
    # We now have the user input a time. We then iterate through package_ids and provide the status of each package in package_ids at the given time.            
    current_time = None
    try:
        time_str = input("Enter time in HH:MM format: ")

        # Parse the input string into a time object
        hours_str, minutes_str = time_str.split(':')
        hours = int(hours_str)
        minutes = int(minutes_str)
        
        current_time = time(hour=hours, minute=minutes)
    except ValueError:
        print("Invalid package id. Please try again.")
            
            
    # print the delivery status and delivery time of all packages represented in package_ids
    for package_id in package_ids:
        # Get, print package status and delivery time
        package_status = get_package_status(package_id, current_time).value
        package = package_hashtable.get(package_id)
        package_delivery_time = package.delivery_time
        
        print(f"Package id: {package_id}. Package status at time {current_time}: {package_status}. Delivery time of package: {package_delivery_time}")
    
    # Compute, then print the total mileage traveled by all trucks
    truck_hours_1 = hours_between(truck_1.depart_time, min(truck_1.return_time, current_time))
    truck_hours_2 = hours_between(truck_2.depart_time, min(truck_2.return_time, current_time))
    truck_hours_3 = hours_between(truck_3.depart_time, min(truck_3.return_time, current_time))

    truck_mileage_1 = truck_hours_1/TRUCK_SPEED
    truck_mileage_2 = truck_hours_2/TRUCK_SPEED
    truck_mileage_3 = truck_hours_3/TRUCK_SPEED

    print(f"Miles traveled by truck 1 at time {current_time}: {truck_mileage_1}")
    print(f"Miles traveled by truck 2 at time {current_time}: {truck_mileage_2}")
    print(f"Miles traveled by truck 3 at time {current_time}: {truck_mileage_3}")            

    
    
    
user_interface()