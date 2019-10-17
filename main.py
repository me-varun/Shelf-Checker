import smtplib
from keras.models import load_model
import cv2
import matplotlib.pyplot as plt
import re
from email.message import EmailMessage
import pytesseract
from unidecode import unidecode


pytesseract.pytesseract.tesseract_cmd="C:\\Program Files (x86)\\Tesseract-OCR\\tesseract.exe"

#Reading The image

img = 'test.jpg'
image = cv2.imread(img)

img = cv2.resize(image,(225,225))
gray = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)
img = img.reshape(1,225,225,3)






#Loading model from the pre-saved model

model = load_model('best_model.h5')


# Predicting Output


out = model.predict(img)

if out[0,0] > out[0,1]:
	print('Shelf is Empty')
	out = 0
else:
	print('Shelf is Not Empty')
	out =1


# Reading The time from the image
#img = 'data/0/20191005_191545753_iOS.jpg'
#img = cv2.imread(img )
#gray = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
#img = imutils.rotate(img,90)
text=pytesseract.image_to_string(gray)
text = unidecode(text)
print(text)
# Pattern to recognize date
pattern = r'[0-9 ]+[:]+[0-9 ]+[:]+[ 0-9]+[ ]*[am]*[pm]*[AM]*[PM]*'
r1 = re.findall(pattern,text)
print(text,r1)
time = r1[0]
print(time)






# EMail sender

#----------------------------------------------------------------------


EMAIL_ADDRESS = 'varungupta117@gmial.com'
#EMAIL_PASSWORD = os.environ.get('EMAIL_PASS')

contacts = ['YourAddress@gmail.com', 'test@example.com']

msg = EmailMessage()
msg['Subject'] = 'Message From the model'
msg['From'] = EMAIL_ADDRESS
msg['To'] = 'YourAddress@gmail.com'
if out == 0:
	msg.set_content(str('The Shelf is Empty at the time '+time))	
else:
	msg.set_content(str('The Shelf is Not Empty at the time'+time))


#with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:

with smtplib.SMTP('localhost', 1025) as smtp:
 
    #smtp.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
    smtp.send_message(msg)

#------------------------------------------------------------------------------'''
