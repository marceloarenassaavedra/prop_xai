from PIL import Image
import math


def direct_image(instance, filename="direct_image.png"):
    size = int(math.sqrt(len(instance)))
    output = Image.new('RGB', (size, size))
    image = [(0, 0, 0) if i == 0 else (255, 255, 255) for i in instance]
    output.putdata(image)
    output = output.resize((size*30, size*30), resample=Image.BOX)
    output.save(filename)

def sufficient_reason_to_image(instance, sufficient_reason, image_filename):
    explanation = [(0, 0, 0) for pixel in instance]

    for i in range(len(instance)):
        if instance[i] == 1:
            explanation[i] = (120, 120, 120)
            if sufficient_reason[i] == 1:
                explanation[i] = (255, 255, 255)
        else:
            if sufficient_reason[i] == 0:
                explanation[i] = (120, 0, 0)

    size = int(math.sqrt(len(instance)))
    output = Image.new("RGB", (size, size))
    output.putdata(explanation)
    output = output.resize((size * 30, size * 30), resample=Image.BOX)
    output.save(image_filename)
    




