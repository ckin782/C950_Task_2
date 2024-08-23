import csv
from Package import Package

# Implementation of a hash table. Uses chaining and a hashtable of length 10 (with a % 10 hash function.) Key is the package id, value is a Package object.
class PackageHashTable:
    def __init__(self):
        self.num_buckets = 10
        self.hashtable = [[] for i in range(self.num_buckets)] # this is the actual hashtable. By default, the value for a given id is None (it hasn't been added yet.)


    def get_hash(self, id):
        '''
        Hash function for the hashtable. Takes an id (key) as input, and returns its hash.
        The hash function computes the hash by simply taking mod self.num_buckets of the given id.
        '''
        id = int(id)
        the_hash = id % self.num_buckets # % 10
        return the_hash
        
    # returns the package (value) for the given id (key)
    def get(self, id):
        '''
        Searches the hashtable for a package with the given id, and returns that package if it exists.
        Otherwise (if there is no package with the given id in the hashtable), returns None.
        '''
        id = int(id)
        key = self.get_hash(id)
        bucket = self.hashtable[key]
        
        # search bucket for package with id
        for package in bucket:
            if int(package.id) == id:
                return package
        
        # if not found, return noe
        return None
    
    def insert(self, id, package):
        '''
        Insert the given package with the given id into the hashtable.
        If a packge with the given id already exists in the hashtable, replace it with the new package information.
        '''
        # locate hash bucket
        bucket_index = self.get_hash(id)
        bucket = self.hashtable[bucket_index]
        bucket_length = len(bucket)
        
        # store the package into the hash bucket
        already_exists = False # true if the packaeg with id is already in hash table
        for i in range(bucket_length):
            package_i = bucket[i]
            id_i = package_i.id
            if id_i == id:
                self.hashtable[bucket_index][i] = package # update existing package to new package
                already_exists = True
                
        if not already_exists:
            self.hashtable[bucket_index].append(package)

    def get_ids(self):
        '''
        Returns a list of every package id present in the hashtable.
        '''
        ids = []
        
        for bucket in self.hashtable:
            for package in bucket:
                ids.append(package.id)
                
        return ids
        