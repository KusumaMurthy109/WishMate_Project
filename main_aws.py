
import subprocess
from rekognition import Rekognition
from linksrecommender import LinksRecommender
from readfile import ReadFile

def main():
    r = Rekognition()
    option = input("camera or upload (type c or u): ")

    while True:
        if option == 'c': #take an image
            r.camera()
            file_path = "/Users/kusumamurthy/Desktop/HackKU/2024/Actual/images" #path to where the images are stored locally
            s3 = "s3://hack-ku-2024/" #where they ae stored in aws S3 bucket

            instruction = f"aws s3 cp {file_path} {s3} --recursive" #the command that goes into the shell
            subprocess.run(instruction, shell=True) #runs the comman in the shell

            camera_wishlist = open("/Users/kusumamurthy/Desktop/HackKU/2024/Actual/camera_wishlist.txt", "w") #opens text file to writ into
                
            photo = f'image1.png'
            bucket = 'hack-ku-2024'
            result = r.image_lable_recognizer(photo, bucket) 
            camera_wishlist.write(','.join(result)) #writes into a text file

            break


        elif option == 'u': #upload image from camera roll
            file_path = "/Users/kusumamurthy/Desktop/HackKU/2024/Actual/images" #path to folder where all teh images will be stored loacally
            s3 = "s3://hack-ku-2024/" #path to where the images will be stored in the aws S3 bucket

            instruction = f"aws s3 cp {file_path} {s3} --recursive" #the command that goes into the shell
            subprocess.run(instruction, shell=True) #runs the comman in the shell

            camera_wishlist = open("/Users/kusumamurthy/Desktop/HackKU/2024/Actual/camera_wishlist.txt", "w") #opens text file to writ into
                
            photo = f'jeacket.png' #image name
            bucket = 'hack-ku-2024' #S3 bucket name
            result = r.image_lable_recognizer(photo, bucket) 
            camera_wishlist.write(','.join(result)) #writes into a text file

            break
        
        else:
            print("Invalid option")

    camera_wishlist.close()
    
    lr = LinksRecommender()

    read_file = ReadFile()

    word_list = read_file.read('camera_wishlist.txt')



    link_n_wishlist = open("/Users/kusumamurthy/Desktop/HackKU/2024/Actual/link_n_wishlist.txt", "w")

    for word in word_list:
        links = lr.links(word)

        link_n_wishlist.write(word)
        link_n_wishlist.write("\n")
        for link in links:
            link_n_wishlist.write(link)
            link_n_wishlist.write("\n")
        
        link_n_wishlist.write("\n")
    
    link_n_wishlist.close()


main()


