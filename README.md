# Phages-cv2
Identify and count plaques

# How to use Phages-cv2
## Installation
***Version:python3.6***
```
# Required package
opencv-python
numpy
pandas
argparse
scikit-learn

# Install
pip3 install -r requirements.txt 
```
It is easy to use:
```
# Help
python phage_img_counts.py -h

usage: phage_img_counts.py [-h] -f FIG_FILE -c CLUSTER
Phages-cv2

optional arguments:
  -h, --help            show this help message and exit
  -f FIG_FILE, --fig_file FIG_FILE
                        Fig file folder
  -c CLUSTER, --cluster CLUSTER
                        Number of corridors that exist
                      
                      
# Example
python phage_img_counts -f phage.jpg -c 7
```

# The graph
![](https://user-images.githubusercontent.com/47686371/166222838-ec6a8a9e-62ce-4967-a455-1ef49ed29fd3.png)

**The red dots represent the identified plaques.** 

# Result
```
# commond line
python phage_img_counts.py -f phage.jpg -c 8

共检测出183个斑点
图片存在的第1个甬道共2个斑点
图片存在的第2个甬道共18个斑点
图片存在的第3个甬道共20个斑点
图片存在的第4个甬道共36个斑点
图片存在的第5个甬道共24个斑点
图片存在的第6个甬道共27个斑点
图片存在的第7个甬道共29个斑点
图片存在的第8个甬道共27个斑点
```
