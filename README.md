# WishMate - HackKU 2024 Project
## WishMate Introduction

This project is created for HackKU 2024, made by Kusuma Murthy, Sophia Jacob, and Anna Lin.

WishMate has been created to serve various non-profit organizations and charitable drives to create a seamless flow between the volunteers and the organizers. WishMate is an app that allows an organizer to create different wishlists for drives like a food drive or a Toys for Tots Drive. Volunteers can then sign up and log in to the App to view drives and wishlists happening near them.

WishMate stemmed from the experiences of teammate, Sophia, who was the Volunteer Coordinator for her Church and ran through several issues when trying to organize food drives, jacket drives, and toy drives. Oftentimes, there would not be enough people that knew about the drive or about the list of items to get. There was no good way to connect between organizations and the volunteers. Therefore, WishMate alleviates this by allowing for organizations and volunteers to interact directly by uploading, viewing, and accessing wishlists for drives.

This will help compell people to volunteer more often for drives and allow organizations to spread their good work to the targetted communities.
## User Manual
Installing the WishMate app is very simple. Start by cloning this GitHub repo as seen below.
```
  git clone git@github.com:KusumaMurthy109/HackKU2024_KSA.git
```

Once it is installed, we can run the following command to make sure that all packages are installed for WishMate. Make sure to run this command in the repo that you have.
```
python3 -m pip install -r requirements.txt
```
Once installed, WishMate will be ready for you to use! Please run the wishmate_login.py file. From there, the Kivy App will come on your screen and you will be able to then interact and create your wishlists and accounts.

## Technologies Used
We built our app using Kivy framework for the front end, Amazon Web Services Rekognition for the image recognition software, and MongoDB atlas for the backend database applications. We constructed the Kivy app using libraries such as Pandas, PyMongo, etc. For AWS Rekognition we used other AWS tools such as S#, IAM, Lambda, etc. We integrated the front as the main source of interaction between the users, and the AWS Rekognition API as well as CV2 (for the camera) was embedded into the frontend to make it seem like a seamless tool. The MongoDB was implemented in the backend and it communicated with both the AWS Rekognition API as well as the Kivy front-end app.
To learn more about MongoDB, please click on this link:
https://www.mongodb.com/languages/python/pymongo-tutorial
To learn more about AWS Rekognition, please click on this link:
https://docs.aws.amazon.com/rekognition/latest/dg/labels-detect-labels-image.html
This project has components powered by AWS Rekognition API and backend work of MongoDB.
