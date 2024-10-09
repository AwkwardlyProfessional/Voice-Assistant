a=20
b=30
total=0
def sumlocal(a,b):
    total=a+b
    print(f"local sum:{total}")
def sumglobal():
    global total
    total=a+b
    print(f"global:{total}")
sumlocal(5, 7)  
print(f"Global total after local sum: {total}") 

sumglobal()  
print(f"Global total after global sum: {total}")