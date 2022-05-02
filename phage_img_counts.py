import cv2
import numpy as np
import pandas as pd
import argparse
from sklearn.cluster import k_means


def phage_nums(dirfile,cluster):
    img0 = cv2.imread(dirfile)
    gray = cv2.cvtColor(img0, cv2.COLOR_BGR2GRAY)
    gauss = cv2.GaussianBlur(gray, (9, 9), 0)

    params = cv2.SimpleBlobDetector_Params()
    # parameter
    params.minThreshold = 100
    params.maxThreshold = 255
    params.thresholdStep = 3.5

    params.filterByColor = True
    # params.blobColor = 0
    params.blobColor = 255

    params.filterByArea = True
    params.minArea = 15
    params.maxArea = 80

    params.filterByCircularity = True
    params.minCircularity = 0.5

    params.filterByConvexity = True
    params.minConvexity = 0.5

    params.filterByInertia = True
    params.minInertiaRatio = 0.3

    detector = cv2.SimpleBlobDetector_create(params)
    keypoints = detector.detect(gauss)

    # im_with_keypoints = cv2.drawKeypoints(img0, keypoints, np.array([]), (0, 0, 255),
    #                                       cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS)

    x_coordinate = []
    y_coordinate = []
    for (x, y) in keypoints[0].convert(keypoints):
        if x > 50 and x < 1100 and y < 1100 and y > 200:
            x_coordinate.append(x)
            y_coordinate.append(500)

    x_coordinate.sort()
    print("共检测出%d个斑点" % len(x_coordinate))
    arr = np.array([x_coordinate, y_coordinate])
    data = pd.DataFrame(arr).T

    model = k_means(data, n_clusters=cluster)

    class_num = list(model[1])
    dict = {}
    for i in class_num:
        if class_num.count(i) >= 1:
            dict[i] = class_num.count(i)

    count = 0
    for key, value in dict.items():
        count = count + 1
        print("图片存在的第%d个甬道共%d个斑点" % (count, dict[key]))


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Phages-cv2")
    parser.add_argument("-f", "--fig_file", required=True, type=str, help="Fig file folder")
    parser.add_argument("-c", "--cluster", required=True, type=str, help="Number of corridors that exist")
    Args = parser.parse_args()

    phage_nums(Args.fig_file,int(Args.cluster))
