# Given an object/dictionary with keys and values that consist of both strings and integers, design an algorithm to calculate and return the sum of all of the numeric values.
# For example, given the following object/dictionary as input:
# You may use whatever programming language you’d like.
# Verbalize your thought process as much as possible before writing any code.
# Utilize UPER while going through thought process.


test = {
 "cat": "bob",
 "dog": 23,
 19: 18,
 90: "fish"
}

total = 0
for i in test:
    if type(test[i]) is int:
        total += test[i]

print(total)