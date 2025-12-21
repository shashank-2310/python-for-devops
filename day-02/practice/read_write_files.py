from pathlib import Path

#Creates demo.txt in SAME folder as THIS script
#Path(__file__).parent = directory containing current script
file = Path(__file__).parent / "demo.txt"
content = "Hello dostooooooooooooooo!!\n"

#Atomic check+create => ensures file exists with default content
if not file.exists():
    file.write_text(content)
    print("Created demo.txt")
print(file.read_text())

# try:
#     with open("demo.txt", "x") as file:  # x' creates new file
#         file.write("Hello dostooooooooooooooo!!\n")
#     print("demo.txt created!\n")
#     with open("demo.txt", "r") as file:
#         print(file.read())
    
# except FileExistsError:
#     print("demo.txt already exists")
#     with open("demo.txt", "r") as file: #'r' is for read mode
#         print(file.read())