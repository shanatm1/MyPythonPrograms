#program no 1:

# program to check if the string is palindrome or not
my_language = "malayalam"

# make it sutable for caseless comparison
my_language = my_language.casefold()

# reverse the string
rev_language = reversed(my_language)

#check the stringis eaqual to its reverse
if list(my_language) == list(rev_language) :
    print("the string is palindrome")
else:
    print("the string is not palindrom")

#program no 2:

my_name = input("enter your name:" )

#print(my_name[:])    #slice function
#print(my_name[0:9])
#print(my_name[0:9:2])

revrse_name = (my_name[::-1])

if my_name == revrse_name:
    print("the name is palindrome")
else:
    print("the name is not palindome")