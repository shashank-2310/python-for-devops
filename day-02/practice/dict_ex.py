from turtle import clear


info = {
    "name" : "Shashank Gupta", #str
    "state" : "Uttarakhand", #str
    "qualification": "B.E.",
    "age" : 22, # int
    "experience": 0.5, # float
    "married": False, # Bool
    "favourites" : ["anime", "movies", "music", 18]
}

print("I'm from ",info["state"]) #Directly accessing value using key
print("I love ", info.get("favourite","Not Found")) #Using .get() method which will give None by default if value not found

info.update({"company": "Capgemini"}) #update: adds a new key-value pair

print(dir(info)) #Gives info about all operations that could be performed on this dict

#Print keys only
# for key in info.keys():
#     print (key)

#Print values only
# for value in info.values():
#     print (value)

#Print keys & values from dict as a list
# for item in info.items():
#     print(item)

#Print keys & values from dict
for key,value in info.items():
    print(key,value)