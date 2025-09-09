## 🚀 Features

* Works with **uEye SDK** + **pyueye**
* Real-time acquisition from two cameras
* Side-by-side video display, scaled to your screen
* Overlap integral plot (updated live)
* Graceful cleanup when exiting with `q`

---

## ⚙️ Requirements

1. **Hardware**

   * Two IDS cameras (tested on `DCC1545M-GL`)

2. **Software**

   * Install the official **IDS uEye Software Suite**
     👉 [Download from IDS Imaging](https://www.1stvision.com/cameras/IDS-imaging-software)
     (choose the version matching your Windows + Python bitness, 64-bit recommended)

   * During installation, ensure:

     * *uEye Camera Manager* and *uEye API (ueye\_api.dll)* are installed
     * Cameras are visible in *uEye Camera Manager*

3. **Python environment**

   ```bash
   pip install pyueye opencv-python matplotlib numpy
   ```

   * `tkinter` usually comes with Python; if not, install it via your OS package manager
   * Make sure you’re running Python with the same bitness (32/64) as your uEye SDK

---

## 📜 Usage

1. **Close ThorCam / uEye Camera Manager** before running this script.
   (They lock the cameras and prevent access.)

2. Run the script:

   ```bash
   python dual_camera_overlap_final.py
   ```

3. Controls:

   * Video window: shows both cameras side by side, resized to full screen width
   * Plot window: overlap integral in real time
   * Press `q` in the video window to exit cleanly

---

## 🔍 How it Works

### Camera initialization

* Each camera is opened by **index** using `ueye.HIDS(0)` and `ueye.HIDS(1)`
* Image memory is allocated via `is_AllocImageMem`
* The display mode is set to **MONO8** (grayscale, 8-bit)
* Capture starts with `is_CaptureVideo`

### Frame acquisition

* Frames are read directly from memory using:

  ```python
  ueye.get_data(mem_ptr, width, height, bits, pitch, copy=False)
  ```
* The raw buffer is reshaped into a NumPy array
* Converted to BGR for OpenCV display

### Overlap integral

* Both frames are converted to grayscale float arrays
* Normalized so their pixel sums equal 1
* Overlap integral:

  $$
  \text{Overlap} = \left(\sum \sqrt{g_1 \cdot g_2}\right)^2
  $$

### Display

* Frames are stacked horizontally
* Automatically resized to match your monitor width (via `tkinter` screen width detection)
* Real-time plot of overlap integral using Matplotlib

### Cleanup

* On exit (`q` key), the script:

  * Stops live video
  * Frees memory
  * Closes the camera handles
  * Destroys all OpenCV windows

---

## 🛠 Troubleshooting

* **`InitCamera failed`** → Close ThorCam/Camera Manager, ensure cameras are connected
* **`DLL not found`** → Add `ueye_api.dll` directory to your `PATH` (e.g., `C:\Program Files\IDS\uEye\Develop\Bin`)
* **No cameras found** → Run *IDS Camera Manager* to confirm cameras are detected
* **Black frames** → Check exposure settings in IDS Camera Manager

---

## 📌 Example Output

* Video window: two camera streams side by side, scaled to your monitor width
* Plot window: real-time overlap integral (0 = dissimilar, 1 = identical images)

---
