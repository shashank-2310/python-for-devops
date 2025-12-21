info = {} # empty dict
print(type(info))

days = set() # empty set
print(type(days))

days = {"saturday","sunday","sunday","saturday"} # duplicates will be removed

nums = [1,1,1,1,2,2,2,3,3,4,6.4,6.4,0,-1,-4]
nums = list(set(nums)) # list with unique values only will be returned
print(nums)

print(dir(days)) #All operations on sets