from app.services.align_images import align_images
from app.services.text_process import cleanup_text
from collections import namedtuple
import pytesseract
import argparse
import imutils
import cv2
import json
from numpy import asarray
import numpy as np
import os

def ocr_image(aligned, template, OCR_Locations):

    print("[Info] OCR'ing document...")
    parsingResults = []
    for loc in OCR_Locations:
        bbox = loc["bbox"]
        (x, y, w, h) = bbox
        roi = aligned[y:h, x:w]

        # ROI coordinates
        rgb = cv2.cvtColor(roi, cv2.COLOR_BGR2GRAY)
        # image = cv2.cvtColor(rgb, cv2.COLOR_BGR2GRAY)
        # cv2.imwrite(loc['id'] + '.jpg', rgb)
        text = pytesseract.image_to_string(rgb, config='--psm 7')
        
        for line in text.split("\n"):
            if len(line) == 0:
                continue

            lower = line.lower()
            count = sum([lower.count(x) for x in loc["filter_keywords"]])

            # if count == 0:
            parsingResults.append((loc, line))

    results = {}
    for (loc, line) in parsingResults:
        r = results.get(loc['id'], None)

        if r is None:
            results[loc['id']] = (line, loc)
        
        else:
            (existingText, loc) = r
            text = "{}\n{}".format(existingText, line)

            results[loc["id"]] = (text, loc)
    return results

def visualize_ocr(results, image, aligned):
    print("[Info] Visualizing OCR...")
    for (locID, result) in results.items():
        (text, loc) = result

        print(loc["id"])
        print("=" * len(loc["id"]))
        print("{}\n\n".format(text))

        (x, y, x2, y2) = loc["bbox"]
        clean = cleanup_text(text)

        cv2.rectangle(aligned, (x, y), (x2, y2), (0, 255, 0), 2)

        for (i, line) in enumerate(clean.split("\n")):
            startY = y + (i * 50) + 40  # Điều chỉnh khoảng cách giữa các dòng và kích thước của chữ
            cv2.putText(aligned, line, (x, startY), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)  # Thay đổi tham số fontScale và thickness

    cv2.imwrite("input.jpg", imutils.resize(image))
    cv2.imwrite("Output.jpg", imutils.resize(aligned))
    print("[Info] aligned image saved as new.jpg")