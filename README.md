# What's on My Plate - iOS App

## Introduction

"What's on My Plate" is an iOS application that captures photos of food and informs the user about the positions of the food on the plate in a clockwise direction. This application uses the FoodSAM model to identify and localize food items.

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
git clone https://gitlab.kit.edu/unidv/whats-on-my-plate.git
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



