

# Project Title: language_learn


## 1. Project Overview

This project is an interactive system that using computer vision in language learning. The system can detect objects in an image and uses a mouse based heatmap to estimate which objects the users is focusing on. It then displays objects label in both the user's native language and target language, and plays the audio in target language(being slow at this moment) to support contextual language learning. 

## 2. Main Features

- Detect objects in imput image
- Generate a heatmap based on mouse movement
- Estimate the current focusing obejct
- Display lables in both users' native language and target language 
- Play target language pronunciation using text to speech(cause of using cpu, showing slowly right now)
## 3. System Pipeline

The overall system pipeline is:

1. Load the input image

2. Detect objects in the image and generate bounding boxes

3. Track mouse movement and generate a heatmap

4. Match the current heat region with detected objects

5. Retrieve the label of the selected object

6. Convert the label into the native language and target language

7. Display the text and play the target-language pronunciation
## 4. Dependencies
This project depends on the following main Python libraries:

- torch
- transformers
- opencv-python
- numpy
- matplotlib
- Pillow
- pynput
- gtts
- playsound

Additional dependencies, if any, should be listed in dutch_learn.yml.
## 5. Installation

1. Clone or download the project code

2. Create and activate a Python environment

3. Install dependencies: `pip install -r dutch_learn.yml`

    

## 6. How to Run


The main entry point of the project is main.py. Run the project with:

`python -m language_learn.main`

After launching, the system loads an image, performs object detection, tracks mouse-based heatmap activity, and displays bilingual labels with target-language speech output when the user focuses on a detected object.

If needed, input image, target language, or label files(now only support livingroom.jpg, but the text_lables can be modified to fit other images) can be modified in the configuration or directly in main.py.

## 7. Project Structure
```
project/
│
├── main.py                  # Main entry point
├── dutch_learn.yml          # Dependency list
├── README.md                # Project documentation
├── imgs/                    # Input images
├── text_labels/             # Label files
├── object_detector/         # Object detection code
├── heatmap/                 # Heatmap generation and update
├── box_visualizer/          # Bounding box and text display
├── speaker/                 # Text-to-speech module
```
## 8. Notes / Limitations

Mouse-based heatmap only approximates user attention and does not fully represent real gaze and need a few second to detect.

Object detection quality depends on model performance, and some objects may be misrecognized.

The text-to-speech module may introduce noticeable latency.

This project focuses on interactive prototype validation rather than large-scale deployment optimization.
## 9. AI Usage Disclosure

AI tools such as ChatGPT were used to assist with report writing and documentation refinement(like grammar check). However, the project design, implementation, debugging, and overall development were completed by the author.

