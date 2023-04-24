import sys
import base64
import io
import imutils
import numpy as np
import cv2
import ast

from imutils import contours
from imutils.perspective import four_point_transform

base64_image_string = sys.argv[1].split(',')[1]
decoded_image_string = base64.b64decode(base64_image_string)

raw_img = cv2.imdecode(np.frombuffer(decoded_image_string, np.uint8), cv2.IMREAD_COLOR)
gray_img = cv2.cvtColor(raw_img, cv2.COLOR_BGR2GRAY)
blurred_img = cv2.GaussianBlur(gray_img, (5, 5), 0)
edged_img = cv2.Canny(blurred_img, 75, 200)

answer_keys = ast.literal_eval(sys.argv[2])

img_contours = cv2.findContours(edged_img.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
img_contours_count = imutils.grab_contours(img_contours)
document_contour = None

if len(img_contours_count) > 0:
    sorted_contours = sorted(img_contours_count, key=cv2.contourArea, reverse=True)

    for contour in sorted_contours:
        contour_perimeter = cv2.arcLength(contour, True)
        approximated_contour = cv2.approxPolyDP(contour, 0.02 * contour_perimeter, True)
        
        if len(approximated_contour) == 4:
            document_contour = approximated_contour
            break

    cv2.drawContours(raw_img, [approximated_contour], 0, (0, 255, 0), 3)

paper = four_point_transform(raw_img, document_contour.reshape(4, 2))            
gray_paper = four_point_transform(gray_img, document_contour.reshape(4, 2))            

binary_gray_paper = cv2.threshold(gray_paper, 0, 255, cv2.THRESH_BINARY_INV | cv2.THRESH_OTSU)[1]
binary_contours = cv2.findContours(binary_gray_paper.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
binary_contours_count = imutils.grab_contours(binary_contours)
question_contours = []

for contour in binary_contours_count:
    x, y, w, h = cv2.boundingRect(contour)
    contour_aspect_ratio = w / float(h)

    if w >= 20 and h >= 20 and contour_aspect_ratio >= 0.9 and contour_aspect_ratio <= 1.1:
        question_contours.append(contour)

sorted_question_contours = contours.sort_contours(question_contours, method="top-to-bottom")[0]
correct_answers = 0

for (q, i) in enumerate(np.arange(0, len(sorted_question_contours), 5)):
    current_question_contours = contours.sort_contours(sorted_question_contours[i:i + 5])[0]
    bubbled = None

    for (j, c) in enumerate(current_question_contours):
        mask = np.zeros(binary_gray_paper.shape, dtype="uint8")
        cv2.drawContours(mask, [c], -1, 255, -1)

        masked_binary_gray_paper = cv2.bitwise_and(binary_gray_paper, binary_gray_paper, mask=mask)
        total_nonzero_pixels = cv2.countNonZero(masked_binary_gray_paper)

        if bubbled is None or total_nonzero_pixels > bubbled[0]:
            bubbled = (total_nonzero_pixels, j)

    bubble_color = (0, 0, 255)
    correct_bubble_option = answer_keys[str(q)]

    if correct_bubble_option == bubbled[1]:
        bubble_color = (0, 255, 0)
        correct_answers += 1

    cv2.drawContours(paper, [current_question_contours[correct_bubble_option]], -1, bubble_color, 3)

test_score = f"{correct_answers} / {len(answer_keys)}"
sys.stdout.write(test_score)
