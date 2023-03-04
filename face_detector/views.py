from django.shortcuts import render

# Create your views here.
# import the necessary packages
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
import numpy as np
# import urllib # python 2
import urllib.request # python 3
import json
import cv2
import os
from django.core.files.uploadedfile import InMemoryUploadedFile

# define the path to the face detector
FACE_DETECTOR_PATH = "{base_path}/haarcascade_frontalface_default.xml".format(
	base_path=os.path.abspath(os.path.dirname(__file__)))

@csrf_exempt
def detect(request):
	# initialize the data dictionary to be returned by the request
	data = {"success": False}
	print(request.POST)
	# check to see if this is a post request
	if request.method == "POST":
	    # check to see if an image was uploaded
		if request.FILES.get("image", None) is not None:
			# grab the uploaded image
			image = _grab_image(stream=request.FILES["image"])
		# otherwise, assume that a URL was passed in
		else:
			# grab the URL from the request
			url = request.POST.get("url", None)
			# if the URL is None, then return an error
			if url is None:
				data["error"] = "No URL provided."
				return JsonResponse(data)
			# load the image and convert
			image = _grab_image(url=url)
		height, width, channels = image.shape


		# convert the image to grayscale, load the face cascade detector,
		# and detect faces in the image
		image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
		detector = cv2.CascadeClassifier(FACE_DETECTOR_PATH)
		rects = detector.detectMultiScale(image, scaleFactor=1.1, minNeighbors=5,
			minSize=(30, 30), flags = cv2.CASCADE_SCALE_IMAGE)
		# construct a list of bounding boxes from the detection
		rectangel = [(int(x), int(y), int(x + w), int(y + h)) for (x, y, w, h) in rects]
		position = GetPosition(rects, image, width, height)
		
		
        
		# update the data dictionary with the faces detected
		data.update({"num_faces": len(rectangel), "faces": rectangel, "success": True, "position": position})
	# return a JSON response
	return JsonResponse(data)

def _grab_image(path=None, stream=None, url=None):
	# if the path is not None, then load the image from disk
	if path is not None:
		image = cv2.imread(path)
	# otherwise, the image does not reside on disk
	else:	
		# if the URL is not None, then download the image
		if url is not None:
			resp = urllib.request.urlopen(url)
			data = resp.read()
		# if the stream is not None, then the image has been uploaded
		elif stream is not None:
			data = stream.read()
		# convert the image to a NumPy array and then read it into
		# OpenCV format
		image = np.asarray(bytearray(data), dtype="uint8")
		image = cv2.imdecode(image, cv2.IMREAD_COLOR)
 
	# return the image
	return image


def GetPosition(faces, img, width, height):
    for (x, y, w, h) in faces:
        cv2.rectangle(img, (x, y), (x+w, y+h), (255, 0, 0), 2)
        posisiX = x
        posisiY = y
        panjangKotak = w
        tinggiKotak = h
	
        panjangGambarAsli = width
        tinggiGambarAsli = height
	
        posisiGarisKotakX = posisiX + panjangKotak / 2;
        posisiGarisKotakY = posisiY + tinggiKotak / 2;

        if posisiGarisKotakX < panjangGambarAsli / 3:
            return "Garis kotak berada di sebelah kiri gambar asli"
        elif posisiGarisKotakX > (2 / 3) * panjangGambarAsli:
            return "Garis kotak berada di sebelah kanan gambar asli"
        elif posisiGarisKotakY < tinggiGambarAsli / 3:
            return "Garis kotak berada di bagian atas gambar asli"
        elif posisiGarisKotakY > (2 / 3) * tinggiGambarAsli:
            return "Garis kotak berada di bagian bawah gambar asli"
        else:
            return  "Garis kotak berada di tengah-tengah gambar asli"