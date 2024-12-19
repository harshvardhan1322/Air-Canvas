# Air Canvas

Air Canvas is an interactive virtual drawing tool that allows users to draw on a digital canvas by detecting gestures or pointer movements captured by a webcam. The tool uses OpenCV to process video input, identify specific color pointers, and track their movements to create drawings.

## Features

- **Real-Time Pointer Tracking**: Tracks colored pointers in real-time using the webcam.
- **Dynamic Color Selection**: Switch between different colors (Blue, Green, Red, Yellow) using on-screen buttons.
- **Clear Canvas**: Clear the entire drawing with a single click on the "CLEAR ALL" button.
- **Adjustable Color Detection**: Fine-tune the HSV range of the color pointer using trackbars for better accuracy.

## Requirements

To run the application, ensure you have the following installed:

- Python 3.x
- OpenCV (`cv2`)
- NumPy

Install the dependencies using pip:

```bash
pip install opencv-python numpy
```

## How It Works

1. **Setup Color Detection**: Adjust the HSV range of the pointer color using the trackbars in the "Color Settings" window.
2. **Draw on the Canvas**: Move a colored pointer (e.g., a marker with a blue cap) in front of the webcam. The tool will track the movement and draw lines on the canvas.
3. **Choose Colors**: Click on the color buttons (Blue, Green, Red, Yellow) to switch between drawing colors.
4. **Clear the Canvas**: Click on the "CLEAR ALL" button to reset the canvas.
5. **Exit the Application**: Press the `q` key to exit the application.

## File Structure

- `main.py`: Contains the core logic of the Air Canvas application.

## Usage

1. Clone or download this repository.
2. Run the script:

   ```bash
   python main.py
   ```

3. Use a colored pointer to start drawing!

## Screenshots

### Color Settings
Adjust HSV ranges for precise color detection.

### Canvas
Interact with the canvas using color pointers.

---

Enjoy drawing with Air Canvas! If you encounter any issues or have feature requests, feel free to open an issue or contribute to the project.

