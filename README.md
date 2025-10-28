# Distributed Image Processing System

## Description
This project implements a Distributed System that efficiently converts High-resolution color images (4K/8K) into Grayscale by dividing the image processing workload across multiple worker nodes.

It is designed for performance, scalability, and ease of deployment in a networked environment, enabling parallel image processing with load balancing and progress tracking.

---

## Group Members and Contributions
This is our school project for Network Programming course, with contribution of 7 members

| Name | Role |
|------|------|
| **Nguyen Thi Minh Nguyet** | System Architect & Leader |
| **Nguyen Quynh Trang** | Image Segmentation & Aggregation |
| **Nguyen Ky Khai** | Master Server Communication |
| **Vu Gia Bach** | Worker Node Implementation |
| **Vuong Ngoc Duy** | Load Balancing & Performance Metrics |
| **Tran Anh Dung** | Image Processing Algorithm & Optimization |
| **Nguyen Hai An** | CLI Interface & Documentation |

## Features

- Master server for task coordination
- Worker clients for parallel image segment processing
- RGB to Grayscale conversion using weighted average method
- Dynamic load balancing based on worker performance
- Real-time progress tracking and estimation
- Support for large image formats (JPG/PNG, up to 8K resolution)
- Result aggregation to reconstruct final grayscale image

---

## System Architecture

```
+-------------------+          +-----------------+
|                   |          |                 |
|   Master Server   +<-------->+   Worker Client |
|                   |          |                 |
+--------+----------+          +-----------------+
         |
         | Distributes image segments
         v
+--------+----------+
|                   |
|  Grayscale Output |
|    (Recombined)   |
|                   |
+-------------------+
```

---

## 📂 Input & Output

- Input: High-resolution color image (`.jpg`, `.png`)
- Output: Grayscale image with the same resolution

---

## Processing Details

- Segmentation: Image is divided into horizontal or vertical segments based on number of workers
- Grayscale Formula:
  ```text
  Gray = 0.299 * R + 0.587 * G + 0.114 * B
  ```
- Each worker:
  - Receives a segment
  - Applies grayscale conversion
  - Sends back the processed segment
  - Reports processing time for performance analysis

---

## Components

| Component        | Description                                 |
|------------------|---------------------------------------------|
| `master_server.py` | Coordinates workers, segments image, merges results |
| `worker_client.py` | Receives, processes, and returns image segments |
| `utils/`           | Utility modules for image I/O and networking |
| `test_images/`     | Sample 4K/8K images for testing             |
| `results/`         | Grayscale output images                     |

---

## Performance Metrics

- Each worker reports:
  - Processing start/end time
  - Segment size
- Master aggregates:
  - Total processing time
  - Speedup gained by adding more workers
  - Worker efficiency

---

## Requirements

- Python 3.8+
- Docker
- NumPy
- Socket programming (standard library)
- Flask

```bash
docker run --rm -it \
  -e NUM_WORKERS=4 \
  -e MASTER_HOST=127.0.0.1 \
  -e MASTER_PORT=5003 \
  -e FLASK_PORT=5006 \
  -p 5003:5003 \
  -p 5006:5006 \
  distgray-backend:latest
```

---

##  Running the System
1. **Start the master server**:
   ```bash
   python master_server.py --image test_images/sample_4k.jpg
   ```

2. **Start worker clients on other machines or terminals**:
   ```bash
   python worker_client.py --host <master_ip> --port 8000
   ```

3. **Wait for completion and check `results/` directory** for grayscale output.

---

## Example Result

| Original Image | Grayscale Output |
|----------------|------------------|
| ![picture](https://github.com/user-attachments/assets/d96bd165-e03e-4e86-b2d2-0ce64e1007f7)
 | ![output](https://github.com/user-attachments/assets/8d33554d-d215-4a4e-8c18-19199600b174)
 |

---

## Documentation

- [x] Distributed processing algorithm
- [x] Image segmentation logic
- [x] Socket communication protocol
- [x] Performance analysis with different worker counts

---

