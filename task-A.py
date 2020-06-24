import json
import re


class bcolors:
    HEADER = "\033[94m"
    GREEN = "\033[92m"
    ENDC = "\033[0m"


with open("comments.json", "r", encoding="utf8") as json_file:
    dataset = json.load(json_file)

# the id of inquiries that is not valid as complaint was extracted manually
not_complaint_id = [
    2464081,
    2470707,
    2474079,
    2567626,
    2582343,
    2581681,
    2538301,
    2501059,
    2501605,
    2497236,
    2497030,
    2493385,
    2492808,
    2491160,
    2459327,
    2457968,
    2496472,
    2472397,
]

count = 0

for data in dataset:
    ID = data["id"]
    subject = data["subject"]
    body = data["cmtbody"]
    channel = data["channel"]

    term = "margin.*term|28 days|28 day|28-day|28-days"
    term2 = "position.*liquidated|trade.*liquidated|position.*closed|trade.*closed"

    # Search in the body of the comment with 'term' and 'term2' key words
    search_body = re.findall(term, body, re.IGNORECASE)
    search_body2 = re.findall(term2, body, re.IGNORECASE)

    if search_body and search_body2:  # both matches found in the comment body
        count += 1
        if ID in not_complaint_id:  # exclude the inquiries, not complaints
            continue
        print(f"{bcolors.GREEN}No. {count}")
        print(f"{bcolors.GREEN}Channel: {channel}")
        print(f"{bcolors.GREEN}MATCH:{search_body} {search_body2} {bcolors.ENDC}")
        print(f"{bcolors.HEADER}ID: {ID}| SUBJECT: {subject} {bcolors.ENDC}")
        print(body)
        print("----------------------")

print(f"{bcolors.GREEN}Total results:", count)
print("Not valid as complaints (counted manually):", len(not_complaint_id))
print("Valid complaints:", count - len(not_complaint_id))
print(len(dataset))
