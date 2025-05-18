# DishDetect: What’s on my plate? – Co-Designing A Mobile App for Clockwise Food Description
[📄 Read the full paper (PDF)](https://dl.acm.org/doi/full/10.1145/3706599.3719689)
## Introduction

DishDetect is an iOS application that captures photos of food and informs the user about the positions of the food on the plate in a clockwise direction. This application uses the FoodSAM model to identify and localize food items.

## Features

- Capture food photos.
- Identify and display the position of food items on a plate in a clockwise direction.

## Technology Stack

- iOS/Swift
- Flask
- FoodSAM

## Installation Guide

### Prerequisites

Ensure your system has the latest version of Python installed. You will also need an iOS development environment and Flask.

### Clone the Repository

```
git clone https://github.com/RuipingL/DishDetect.git
cd Whats on my Plate
```

### Install Dependencies

First, install FoodSAM by cloning its GitHub repository:

```
git clone [https://github.com/jamesjg/FoodSAM](https://github.com/jamesjg/FoodSAM)
cd FoodSAM
```

Install the necessary dependencies for FoodSAM.

### Configure the Flask Application

Place the `app.py` and `describe.py` files in the root directory of the FoodSAM project.
Run the Flask application:

```
python app.py
```

### Configure the iOS Application

1. Open `test01.xcodeproj`.
2. Update the server IP address in `ContentView.swift`. If using the free version of ngrok, follow these steps:
   - Download and install ngrok from: https://ngrok.com/download
   - Run the following command to map local port 5000 to a public IP:
     ```
     ngrok http 5000
     ```
   - Update the generated public IP address in `ContentView.swift`.

### Run the iOS Application

Compile and run the application in Xcode. Ensure the device can access the configured server address.

## Usage

Open the application and follow the instructions to take photos of food and obtain position information.


## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE) file for details.

## 📖 Citation

If you find **DishDetect: What’s on my plate? – Co-Designing A Mobile App for Clockwise Food Description** helpful in your research or projects, please cite our CHI EA 2025 paper:

```bibtex
@inproceedings{10.1145/3706599.3719689,
  author    = {Ying, Kedi and Tao, Mingzhe and Dai, Ruize and Liu, Ruiping and M\"{u}ller, Karin and Jaworek, Gerhard and Zhang, Jiaming and Stiefelhagen, Rainer},
  title     = {DishDetect: What’s on my plate? – Co-Designing A Mobile App for Clockwise Food Description},
  booktitle = {Proceedings of the Extended Abstracts of the CHI Conference on Human Factors in Computing Systems},
  year      = {2025},
  publisher = {Association for Computing Machinery},
  address   = {New York, NY, USA},
  doi       = {10.1145/3706599.3719689},
  url       = {https://doi.org/10.1145/3706599.3719689},
  articleno = {193},
  numpages  = {7},
  isbn      = {9798400713958},
  keywords  = {Visual impairment, iOS application, Semantic segmentation, Food classification},
  series    = {CHI EA '25}
}
