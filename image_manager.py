import random


ALL_IMAGES = [

    "images/image1.jpg",
    "images/image2.jpg",
    "images/image3.jpg",
    "images/image4.jpg",
    "images/image5.jpg",
    "images/image6.jpg"
]


def get_morning_image(user):

    return random.choice(
        ALL_IMAGES
    )