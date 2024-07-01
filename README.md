# PhotoGroupAI
![image](https://github.com/UltraDeveloper7/PhotoGroupAI/assets/75303541/5c3d9c66-35d0-4bfc-ac75-16417a832371)

## Overview
This repository contains the source code for PhotoGroupAI, an application that clusters and organizes images using machine learning. The application provides a graphical user interface (GUI) to select folders, configure clustering settings, and organize images into groups.

## Table of Contents
1. [Features](#features)
2. [Technologies Used](#technologies-used)
3. [Prerequisites](#prerequisites)
4. [Installation](#installation)
    - [Clone from GitHub](#clone-from-github)
    - [Download as ZIP](#download-as-zip)
5. [Usage](#usage)
6. [Running the Application](#running-the-application)
7. [Directory Structure](#directory-structure)
8. [Scripts](#scripts)
9. [Contributing](#contributing)
10. [License](#license)
11. [Contact](#contact)
12. [Acknowledgements](#acknowledgements)

## Features
- Cluster images using KMeans or DBSCAN algorithms.
- Configure clustering parameters via GUI.
- Move or copy clustered images into organized folders.
- Real-time progress updates.

## Technologies Used
- Python
- Keras
- TensorFlow
- PySide6
- PIL
- NumPy
- Scikit-learn

## Prerequisites
Before you begin, ensure you have met the following requirements:
- Python 3.6 or later installed

## Installation
You can install the application by either cloning it from GitHub or downloading it as a ZIP file.

### Clone from GitHub
1. Clone the repository:
    ```bash
    git clone https://github.com/UltraDeveloper7/PhotoGroupAI.git
    cd PhotoGroupAI
    ```

### Download as ZIP
1. Download the ZIP file from GitHub:
    - Go to the [repository page](https://github.com/YourUsernamUltraDeveloper7/PhotoGroupAI).
    - Click on the "Code" button and select "Download ZIP".
    - Extract the downloaded ZIP file.
    - Navigate to the extracted directory:
    ```bash
    cd PhotoGroupAI
    ```

2. Install the dependencies:
    ```bash
    pip install -r requirements.txt
    ```

## Usage
To use PhotoGroupAI, follow the instructions in the "Running the Application" section to start the GUI application. You can select a folder containing images, configure clustering settings, and start the clustering process.

## Running the Application

1. **Run the GUI**:
   - Launch the GUI using `app.py`:
     ```bash
     python app.py
     ```

2. **Instructions**:
   1. **Open the Application**:
      - Launch the PhotoGroupAI application.

   2. **Select a Folder**:
      - Click on the "Select Folder" button to choose a directory containing the images you want to cluster.

   3. **Configure Clustering Settings**:
      - Choose the clustering algorithm (KMeans or DBSCAN).
      - Set the number of clusters for KMeans or the `eps` and `min_samples` parameters for DBSCAN.
      - Optionally, enable the "Move Files" checkbox to move images instead of copying them.

   4. **Run the Clustering**:
      - Click the "Run" button to start the clustering process.
      - Monitor the progress through the progress bar and status messages.

## Directory Structure
```
PhotoGroupAI/
├── README.md
├── requirements.txt
├── worker.py
├── image_clusterer.py
├── dbscan_parameters_dialog.py
├── app.py
```

## Scripts
- `worker.py`: Contains the `Worker` and `WorkerSignals` classes for handling background tasks.
- `image_clusterer.py`: Contains the `ImageClusterer` class for extracting features and clustering images.
- `dbscan_parameters_dialog.py`: Contains the `DBSCANParametersDialog` class for configuring DBSCAN parameters.
- `app.py`: Contains the main GUI application.

## Contributing
1. Fork the repository
2. Create your feature branch (`git checkout -b feature/YourFeature`)
3. Commit your changes (`git commit -m 'Add some feature'`)
4. Push to the branch (`git push origin feature/YourFeature`)
5. Open a pull request

## License
This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Contact
If you have any questions or issues, please contact [konstantinostoutounas@gmail.com](mailto:konstantinostoutounas@gmail.com).

## Acknowledgements
- Special thanks to the contributors and open-source libraries that made this project possible.

---

Thank you for using PhotoGroupAI! Happy clustering!
