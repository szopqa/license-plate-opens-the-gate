import os
import numpy as np
from sklearn.svm import SVC
from sklearn.model_selection import cross_val_score
from sklearn.externals import joblib
from skimage.io import imread
from skimage.filters import threshold_otsu

from plate_recognition_core.Reader import Reader

# # # # # # # # # # # # # # # #
#  Script used to train model #
# # # # # # # # # # # # # # # #

letters = [
            '0', '1', '2', '3', '4', '5', '6', '7', '8', '9', 'A', 'B', 'C', 'D',
            'E', 'F', 'G', 'H', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T',
            'U', 'V', 'W', 'X', 'Y', 'Z'
        ]

def read_training_data(training_directory):
    image_data = []
    target_data = []
    for each_letter in os.listdir(f'{training_directory}'):
        for filename in os.listdir(f'{training_directory}/{each_letter}'):
            print(f'DEBUG: Learning letter {each_letter} from file : {filename}')

            image_path = os.path.join(training_directory, each_letter, filename)
            img_details = imread(image_path, as_gray=True)
            reader = Reader(image_path)
            # converts each character image to binary image
            binary_image = reader.get_binary_fixed_resize(20, 20)
            flat_bin_image = binary_image.reshape(-1)
            image_data.append(flat_bin_image)
            target_data.append(each_letter)

    return (np.array(image_data), np.array(target_data))

def cross_validation(model, num_of_fold, train_data, train_label):
    # dividing the dataset into 4 and useing 1/4 of it for testing
    # and the remaining 3/4 for the training
    accuracy_result = cross_val_score(model, train_data, train_label,
                                      cv=num_of_fold, n_jobs=-1)
    print("Cross Validation Result for ", str(num_of_fold), " -fold")

    print(accuracy_result * 100)


current_dir = os.path.dirname(os.path.realpath(__file__))

training_dataset_dir = os.path.join(current_dir, '../train_data')

image_data, target_data = read_training_data(training_dataset_dir)

svc_model = SVC(kernel='linear', probability=True, verbose=True)

cross_validation(svc_model, 4, image_data, target_data)

# training model
svc_model.fit(image_data, target_data)

# saving trained model to file
save_directory = os.path.join(current_dir, 'models/svc/')
if not os.path.exists(save_directory):
    os.makedirs(save_directory)
joblib.dump(svc_model, save_directory+'/svc.pkl')