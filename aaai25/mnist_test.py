from mnist_data import *
from linear_model import LinearModel
import random
from vis_exp import *
from MSR import compute_MSR, compute_delta_MSR

def test_linear(digit):
    images, labels, test_images, test_labels = setup(28)
    sk_model = generate_linear(images, labels, digit)
    expected = simplify_to_digit(test_labels, digit)
    predicted = sk_model.predict(test_images)
    acc = accuracy_score(expected, predicted)
    print(f"Digit = {digit}, accuracy = {acc}")
    
    
def test_digits():
    for d in range(0, 10):
        test_linear(d)
        
        
def test_MSR(digit):
    images, labels, test_images, test_labels = setup(28)
    test_labels = simplify_to_digit(test_labels, digit)
    sk_model = generate_linear(images, labels, digit)
    linear = LinearModel.from_SKLearn(sk_model)

    for i in range(50):
        index = random.randint(0, len(test_images)-1)
        img = test_images[index]
        label = test_labels[index]
        direct_image(img, f"images/img_{index}_d_{label}.png")
        ev = linear.eval(img)
        msr_size, msr_partial = compute_MSR(linear, img)
        sufficient_reason_to_image(img, msr_partial, f"images/msr_{index}.png")
        print("eval:", ev, "label:", label, " MSR size: ", msr_size)
        
        
def test_delta_MSR(digit):
    images, labels, test_images, test_labels = setup(16)
    test_labels = simplify_to_digit(test_labels, digit)
    sk_model = generate_linear(images, labels, digit)
    linear = LinearModel.from_SKLearn(sk_model)

    delta = 0.75
    for i in range(50):
        index = random.randint(0, len(test_images)-1)
        img = test_images[index]
        label = test_labels[index]
        if label != digit:
            continue
        direct_image(img, f"images/img_{index}_d_{label}.png")
        ev = linear.eval(img)
        msr_size, msr_partial, delta_star = compute_delta_MSR(linear, img, delta=delta, epsilon=0.2, gamma=0.2)
        sufficient_reason_to_image(img, msr_partial, f"images/msr_{index}_{msr_size}_{delta_star:.2f}.png")
        print("eval:", ev, "label:", label, " MSR size: ", msr_size)
        
    
test_delta_MSR(1)
    


    

