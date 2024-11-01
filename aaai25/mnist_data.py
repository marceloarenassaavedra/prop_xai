from mnist import MNIST


from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score
from PIL import Image
import math

import numpy as np

import os


# Load dataset
def setup(reduced_dim=20, filter_digits=None):
    print("Setting up dataset...")
    dir_path = os.path.dirname(os.path.abspath(__file__))
    dataset_path = os.path.join(dir_path, './datasets/mnist/')
    mndata = MNIST(dataset_path)
    images, labels = mndata.load_training()
    test_images, test_labels = mndata.load_testing()
    images = binarize_images(images)
    images = [reduce_dim(image, reduced_dim) for image in images]
    test_images = binarize_images(test_images)
    test_images = [reduce_dim(image, reduced_dim) for image in test_images]
    if filter_digits is not None:
        images, labels = filter_d(images, labels, filter_digits)
        test_images, test_labels = filter_d(test_images, test_labels, filter_digits)
    print("Dataset loaded!")
    return images, labels, test_images, test_labels


def filter_d(images, labels, digits):
    filtered_images = []
    filtered_labels = []
    assert len(images) == len(labels)
    for i in range(len(images)):
        if labels[i] in digits:
            filtered_images.append(images[i])
            filtered_labels.append(labels[i])
    return filtered_images, filtered_labels

def binarize(image):
    result = [0 for _ in image]
    for i in range(len(image)):
        result[i] = (image[i] > 70)
    return result


def binarize_images(images):
    for i, image in enumerate(images):
        images[i] = binarize(image)
    return images


def load_test_images(reduced_dim=20):
    dir_path = os.path.dirname(os.path.abspath(__file__))
    dataset_path = os.path.join(dir_path, './datasets/mnist/')
    mndata = MNIST(dataset_path)
    images, labels = mndata.load_testing()
    binarized_images = binarize_images(images)
    return [reduce_dim(image, reduced_dim) for image in binarized_images], labels


def reduce_dim(flat_image, dim):
    size = int(math.sqrt(len(flat_image)))
    output = Image.new('1', (size, size))
    output.putdata(flat_image)
    reduced = output.resize((dim, dim), resample=Image.BOX)
    data = list(reduced.getdata())
    return data
    

def simplify_to_digit(labels, digit):
    return [int(label == digit) for label in labels]
    
    
def generate_linear(images, labels, digit):
    print("Generating linear model...")
    lbls = simplify_to_digit(labels, digit)
    data_size = 60000
    train_x = images[:data_size]
    train_y = lbls[:data_size]
    model = LogisticRegression()
    print("Starting training...")
    model.fit(train_x, train_y)
    print("Finished training!")
    return model 
    
    

    


# def generate_dt(images, labels, digit, n_leaves):
#     lbls = simplify_to_digit(labels, digit)
#     dt = DecisionTreeClassifier(
#         random_state=0,
#         max_leaf_nodes=n_leaves,
#         splitter='random',
#         class_weight='balanced'
#     )
#     data_size = 60000
#     train_x = images[:data_size]
#     train_y = lbls[:data_size]
#     dt.fit(train_x, train_y)
#     return dt


# def train_tree(
#     images,
#     labels,
#     test_images,
#     test_labels,
#     digit,
#     n_leaves,
#     filename,
# ):
#     dt = generate_dt(images, labels, digit, n_leaves)
#     expected = simplify_to_digit(test_labels, digit)

#     predicted = dt.predict(test_images)
#     acc = accuracy_score(expected, predicted)

#     dimension = len(images[0])
#     size = int(math.sqrt(dimension))

#     ft_names = [f'pixel ({i//size}, {i%size})' for i in range(dimension)]
#     ft_types = ['boolean' for _ in range(dimension)]
#     index_pos = dt.classes_.tolist().index(1)
#     index_neg = dt.classes_.tolist().index(0)
#     class_names = [None, None]
#     class_names[index_pos] = f'is {digit}'
#     class_names[index_neg] = f'is not {digit}'
#     positive_class = class_names[index_pos]
#     dtree.serialize_tree_to_json(filename, dt, ft_names, ft_types, class_names, positive_class, acc)
#     return dt, acc


def vis_test_image(index_img):
    images, _ = load_test_images()
    size = 20
    image = reduce_dim(images[index_img], size)

    
    output = Image.new('RGB', (size, size))
    output.putdata(image)

    output = output.resize((size*30, size*30), resample=Image.BOX)
    output.show()

