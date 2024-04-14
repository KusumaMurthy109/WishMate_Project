# Copyright 2018 Amazon.com, Inc. or its affiliates. All Rights Reserved.
# SPDX-License-Identifier: MIT-0 (For details, see https://github.com/awsdocs/amazon-rekognition-developer-guide/blob/master/LICENSE-SAMPLECODE.)

import boto3
import cv2
import os 

class Rekognition:
    def camera(self): #this code captures the image
        cam_port = 0 #camera port
        cam = cv2.VideoCapture(cam_port) #this opens the camera

        n=0
        while True:
            n = n+1

            ret, image = cam.read()
            cv2.imshow("Press any key to capture", image)

            key = cv2.waitKey(1) #captures the image uopn a click of a button

            if key != -1: #runs this code once the a button on the keyboard is clicked
                output = "images"
                os.makedirs(output,exist_ok = True)
                cv2.imwrite(os.path.join(output, f"image{1}.png"), image) #addds the image into a folder on my local machine
                break
        
        cv2.waitKey(0) #closes the camera windon upon a click of a button on the keyboard
        cv2.destroyAllWindows() #close the camera window


    def image_lable_recognizer(self, photo, bucket):
        session = boto3.Session()
        client = session.client('rekognition')

        response = client.detect_labels(
            Image={'S3Object':{'Bucket': bucket, 'Name': photo}}, #gets the image from the aws S3 bucket
            MaxLabels=5
        )
        label_list = []
        for label in response['Labels']: #appends the recognized lables into a list
            label_list.append(label['Name'])
        return label_list #returns the list




