"""
hashmap.py
author: Glenn Gorgoth
Nov 4, 2020

"""

class HashMap():
    """description"""

    #INIT Methods
    def __init__(self):
        self.buckets = [None] * 8

    # Mutator Methods
    def rehash(self):
        """makes a new hashmap with twice as many buckets"""
        new_buckets = [None] * self.capacity() * 2
        for j in range(len(self.buckets)):
            new_buckets[j] = self.buckets[j]
        self.buckets = new_buckets

    def set(self, key, value):
        """creates a new Entry in the hashmap with a key and value"""
        entry = Entry(key, value)
        for i in range(len(self.buckets)):
            if self.buckets[i] is None:
                self.buckets[i] = entry
                break
            if self.buckets[i].key == key:
                self.buckets[i].value = value
                break
        if self.size() >= self.capacity() * .8:
            new_buckets = [None] * self.capacity() * 2
            for j in range(len(self.buckets)):
                new_buckets[j] = self.buckets[j]
            self.buckets = new_buckets

    # Getter Methods
    def clear(self):
        """erases all buckets, restarts with 8 empty buckets"""
        self.buckets = [None] * 8

    def get(self, key, default=None):
        """returns value for 'key' or the default value if
        that key doesn't exist"""
        for i in self.buckets:
            if i is None:
                return default
            if i.key == key:
                return i.value
        return default

    def capacity(self):
        """returns the number of buckets"""
        return len(self.buckets)

    def size(self):
        """returns the number of items in hashmap"""
        counter = 0
        for i in self.buckets:
            if i is not None:
                counter += 1
        return counter

    def keys(self):
        """returns a list of all keys in hashmap"""
        lyst = []
        for i in self.buckets:
            if i is None:
                return lyst
            lyst.append(i.key)
        return lyst

    def values(self):
        """returns list of all values in hashmap"""
        lyst = []
        for i in self.buckets:
            if i is None:
                return lyst
            lyst.append(i.value)
        return lyst

    def sort(self, num):
        """sorts the hashmap by value, highest to lowest.
        returns the first 'num' number of items"""
        keys = self.keys()
        values = self.values()
        sorted_items = sorted(zip(values, keys), reverse=True)
        sorted_items = sorted_items[:num]
        return sorted_items
    
    def asc_sort(self):
        """sorts the hashmap by value, lowest to highest."""
        keys = self.keys()
        values = self.values()
        sorted_items = sorted(zip(values, keys))
        return sorted_items
    
    def swap_sort(self):
        keys = self.keys()
        values = self.values()
        sorted_items = sorted(zip(keys, values), reverse=True)
        return sorted_items

class Entry():
    """Represents a dictionary entry.
    Supports compariosons by key."""

    def __init__(self, key, value):
        """creates a new entry with key and value"""
        self.key = key
        self.value = value

    def __str__(self):
        """for printing the entry"""
        return str(self.key) + ":" + str(self.value)
