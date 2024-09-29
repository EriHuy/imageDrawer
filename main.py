import numpy as np
import cv2
import turtle
import time

def sobel_edge_detection(image):
    gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    blurred_image = cv2.GaussianBlur(gray_image, (3, 3), 0)

    Gx = cv2.Sobel(blurred_image, cv2.CV_64F, 1, 0, ksize=3)
    Gy = cv2.Sobel(blurred_image, cv2.CV_64F, 0, 1, ksize=3)

    G = np.sqrt(Gx**2 + Gy**2)

    #Gx = np.uint8(255 * np.abs(Gx) / np.max(Gx))
    #Gy = np.uint8(255 * np.abs(Gy) / np.max(Gy))
    G = np.uint8(255 * G / np.max(G))

    return G

def median_filter(image):
    image_h = image.shape[0]
    image_w = image.shape[1]

    image_new = np.zeros([image_h, image_w])

    for i in range(1, image_h-1): 
        for j in range(1, image_w-1): 
            temp = [image[i-1, j-1], 
                image[i-1, j], 
                image[i-1, j + 1], 
                image[i, j-1], 
                image[i, j], 
                image[i, j + 1], 
                image[i + 1, j-1], 
                image[i + 1, j], 
                image[i + 1, j + 1]] 
            
            temp = sorted(temp) 
            image_new[i, j]= temp[4] 
    
    image_new = image_new.astype(np.uint8)

    return image_new
    
def invertColors(image):
    image = cv2.bitwise_not(image)

    kernel = np.array([[0, -1, 0], [-1, 5, -1], [0, -1, 0]]) 

    sharpened_image = cv2.filter2D(image, -1, kernel) 

    return sharpened_image


def draw(image):

    start = time.time()

    image = cv2.cvtColor(image, cv2.COLOR_BAYER_BG2BGR)

    image_height = image.shape[0]
    image_width = image.shape[1]
    
    if image_height >= 600 or image_width >= 600:
        image = cv2.resize(image, (int(image_height/2), int(image_width/2)))

        image_height = image.shape[0]
        image_width = image.shape[1]
 
    screen = turtle.Screen()
    screen.setup(width=image_width, height=image_height)
    screen.colormode(255)

    drawer = turtle.Turtle()
    drawer.speed(0) 
    drawer.penup()

    start_x = -image_width / 2
    start_y = (image_height / 2) + 4
    drawer.goto(start_x, start_y)

    turtle.tracer(n=5, delay=0)
    drawer.ht()

    for y in range(image_height):
        for x in range(image_width):

            b, g, r = image[y, x]
            
            drawer.goto(start_x + x, start_y - y)
            if r <= 220 and g <= 220:
                #drawer.pencolor(44, 44, 44)
                drawer.pendown()
                drawer.dot(1) 
            else:
                drawer.penup()
        
    end = time.time()
    print(f"Drawing time: {end}")

    turtle.done()

    

def main():

    image = cv2.imread("images/cat.png")

    filtered_image = sobel_edge_detection(image)

    filtered_image = median_filter(filtered_image)

    filtered_image = invertColors(filtered_image)

    cv2.imshow("Original", image)
    cv2.imshow("Filtered", filtered_image)

    draw(filtered_image)


if __name__ == "__main__":
    main()