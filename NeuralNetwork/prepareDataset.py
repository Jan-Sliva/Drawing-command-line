import os.path as P
import os

FOLDER = "D:\\extracted_images"

for fold in os.listdir(FOLDER):
    path = P.join(FOLDER, fold)
    if not P.isdir(path):
        continue
    sezn = os.listdir(path)
    sezn = list(filter(lambda x: not "exp" in x, sezn))
    print(fold + " " + str(len(sezn)))


