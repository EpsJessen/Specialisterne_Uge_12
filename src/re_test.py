import re

check = re.search('[(][0-9]+[)]$', "dagger (65)")
if check:
    print(check.group()[1:-1])

if re.match("([A-Z]|[0-9]|.| )*$", "HI"):
    print("HI")
if re.match("([A-Z]|[0-9]|[.]| )+$", ""):
    print("Hi")
if re.match("([A-Z]|[0-9]|[.]|\s)+$", "HI"):
    print("15.4")

if re.match("[#]+ ([A-Z])+", "### A"):
    print("### *A")
else:
    print("not ### *A")