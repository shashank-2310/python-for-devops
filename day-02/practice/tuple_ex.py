a = (1, 2, 3, 'Jenkins', "GitHub", True, 1, -1, 0.6)
print(type(a))
print(a)
print(a[2])

print(a.index(-1)) #Returns 1st occurence of the given element
print(a.index('GitHub'))
print(a.index(1, 4)) #Returns 1st occurence of 1 after 4th index

print(a.count(1)) #Return count of the element =>  Count of 1 is 3 as True = 1

print(dir(a)) #All operations on tuple

#a[4] = 'GitLab' => Error

#Iterate thru a tuple
for item in a:
    print(item)

#Check if an element exists in a tuple
print(7 in a)

#Deleting individual items of a tuple is not possible
#Deleting the tuple itself is possible
b = (6, 7, 8, 9, 'Linux')
del b


