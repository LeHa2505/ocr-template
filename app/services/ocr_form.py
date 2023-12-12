import align_images
from collections import namedtuple
import pytesseract
import argparse
import imutils
import cv2
import json

def cleanup_text(text):
    return "".join([c if ord(c) < 128 else "" for c in text]).strip()

ap = argparse.ArgumentParser()
ap.add_argument("-i", "--image", required=True,
    help="path to input image that we'll assign to template")
ap.add_argument("-t", "--template", required=True,
    help="path to input template image")
args = vars(ap.parse_args())

with open("config.json", "r") as config_file:
    OCR_Locations = json.load(config_file)

print("[Info] loading images...")
image = cv2.imread(args["image"])
template = cv2.imread(args["template"])

print("[Info] aligning images...")
aligned = align_images.align_images(image, template)

print("[Info] OCR'ing document...")
parsingResults = []

for loc in OCR_Locations:
    bbox = loc["bbox"]
    (x, y, w, h) = bbox
    # roi = aligned[y:y+h, x:x+w]
    roi = aligned[y: h, x: w]

    rgb = cv2.cvtColor(roi, cv2.COLOR_BGR2RGB)
    text = pytesseract.image_to_string(rgb)
    
    for line in text.split("\n"):
        if len(line) == 0:
            continue

        lower = line.lower()
        count = sum([lower.count(x) for x in loc["filter_keywords"]])

        # if count == 0:
        parsingResults.append((loc, line))

results = {}

for (loc, line) in parsingResults:
    print("loc:", loc)
    r = results.get(loc['id'], None)

    if r is None:
        results[loc['id']] = (line, loc)
    
    else:
        (existingText, loc) = r
        text = "{}\n{}".format(existingText, line)

        results[loc["id"]] = (text, loc)

for (locID, result) in results.items():
    (text, loc) = result

    print(loc["id"])
    print("=" * len(loc["id"]))
    print("{}\n\n".format(text))

    (x, y, w, h) = loc["bbox"]
    clean = cleanup_text(text)

    cv2.rectangle(aligned, (x, y), (x+w, y+h), (0, 255, 0), 2)

    for (i, line) in enumerate(clean.split("\n")):
        startY = y + (i * 70) + 40
        cv2.putText(aligned, line, (x, startY), cv2.FONT_HERSHEY_SIMPLEX, 1.8, (0, 0, 255), 5)

cv2.imwrite("input.jpg", imutils.resize(image))
cv2.imwrite("Output.jpg", imutils.resize(aligned))
print("[Info] aligned image saved as new.jpg")
# cv2.imshow("Input", imutils.resize(image))
# cv2.imshow("Output", imutils.resize(aligned))
cv2.waitKey(0)