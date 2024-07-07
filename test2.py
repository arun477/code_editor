import sys
import os
import pika
import json
import time
import logging
from PIL import Image, ImageEnhance
from io import BytesIO
import base64
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLabel, QListWidget, QProgressBar, QFileDialog, QComboBox
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt, QThread, pyqtSignal

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# RabbitMQ connection parameters
RABBITMQ_HOST = 'localhost'
UPLOAD_QUEUE = 'image_upload'
PROCESSING_QUEUE = 'image_processing'
COMPLETED_QUEUE = 'image_completed'
ERROR_QUEUE = 'image_error'

# Image processing functions
def apply_filter(image, filter_type):
    if filter_type == 'sepia':
        sepia_filter = Image.new('RGB', image.size, (255, 240, 192))
        return Image.blend(image, sepia_filter, 0.5)
    elif filter_type == 'grayscale':
        return image.convert('L')
    elif filter_type == 'enhance':
        enhancer = ImageEnhance.Contrast(image)
        return enhancer.enhance(1.5)
    else:
        return image

class ImageProcessingWorker(QThread):
    update_signal = pyqtSignal(dict)
    
    def __init__(self):
        super().__init__()
        self.running = True

    def run(self):
        connection = pika.BlockingConnection(pika.ConnectionParameters(RABBITMQ_HOST))
        channel = connection.channel()

        channel.queue_declare(queue=UPLOAD_QUEUE, durable=True)
        channel.queue_declare(queue=PROCESSING_QUEUE, durable=True)
        channel.queue_declare(queue=COMPLETED_QUEUE, durable=True)
        channel.queue_declare(queue=ERROR_QUEUE, durable=True)

        def process_callback(ch, method, properties, body):
            image_info = json.loads(body)
            try:
                image_data = base64.b64decode(image_info['image_data'])
                image = Image.open(BytesIO(image_data))
                processed_image = apply_filter(image, image_info['filter'])
                output = BytesIO()
                processed_image.save(output, format='JPEG')
                image_info['processed_data'] = base64.b64encode(output.getvalue()).decode('utf-8')
                del image_info['image_data']
                channel.basic_publish(
                    exchange='',
                    routing_key=COMPLETED_QUEUE,
                    body=json.dumps(image_info),
                    properties=pika.BasicProperties(delivery_mode=2)
                )
                self.update_signal.emit({'stage': 'processed', 'data': image_info})
            except Exception as e:
                logger.error(f"Error processing image {image_info['id']}: {str(e)}")
                channel.basic_publish(
                    exchange='',
                    routing_key=ERROR_QUEUE,
                    body=json.dumps({'id': image_info['id'], 'error': str(e)}),
                    properties=pika.BasicProperties(delivery_mode=2)
                )
            finally:
                ch.basic_ack(delivery_tag=method.delivery_tag)

        channel.basic_qos(prefetch_count=1)
        channel.basic_consume(queue=PROCESSING_QUEUE, on_message_callback=process_callback)

        while self.running:
            channel.connection.process_data_events(time_limit=1)

        channel.close()
        connection.close()

    def stop(self):
        self.running = False

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Interactive Image Processing Pipeline")
        self.setGeometry(100, 100, 800, 600)

        main_widget = QWidget()
        self.setCentralWidget(main_widget)
        main_layout = QHBoxLayout()
        main_widget.setLayout(main_layout)

        left_widget = QWidget()
        left_layout = QVBoxLayout()
        left_widget.setLayout(left_layout)
        main_layout.addWidget(left_widget)

        self.upload_button = QPushButton("Upload Image")
        self.upload_button.clicked.connect(self.upload_image)
        left_layout.addWidget(self.upload_button)

        self.filter_combo = QComboBox()
        self.filter_combo.addItems(['sepia', 'grayscale', 'enhance'])
        left_layout.addWidget(self.filter_combo)

        self.process_button = QPushButton("Process Image")
        self.process_button.clicked.connect(self.process_image)
        self.process_button.setEnabled(False)
        left_layout.addWidget(self.process_button)

        self.status_list = QListWidget()
        left_layout.addWidget(self.status_list)

        right_widget = QWidget()
        right_layout = QVBoxLayout()
        right_widget.setLayout(right_layout)
        main_layout.addWidget(right_widget)

        self.original_label = QLabel("Original Image")
        self.original_label.setAlignment(Qt.AlignCenter)
        right_layout.addWidget(self.original_label)

        self.processed_label = QLabel("Processed Image")
        self.processed_label.setAlignment(Qt.AlignCenter)
        right_layout.addWidget(self.processed_label)

        self.worker = ImageProcessingWorker()
        self.worker.update_signal.connect(self.update_ui)
        self.worker.start()

        self.image_path = None

    def upload_image(self):
        file_dialog = QFileDialog()
        self.image_path, _ = file_dialog.getOpenFileName(self, "Select Image", "", "Image Files (*.png *.jpg *.bmp)")
        if self.image_path:
            pixmap = QPixmap(self.image_path)
            self.original_label.setPixmap(pixmap.scaled(400, 300, Qt.KeepAspectRatio, Qt.SmoothTransformation))
            self.process_button.setEnabled(True)
            self.status_list.addItem(f"Uploaded: {os.path.basename(self.image_path)}")

    def process_image(self):
        if not self.image_path:
            return

        with open(self.image_path, "rb") as image_file:
            image_data = base64.b64encode(image_file.read()).decode('utf-8')

        image_info = {
            'id': str(time.time()),
            'filter': self.filter_combo.currentText(),
            'image_data': image_data
        }

        connection = pika.BlockingConnection(pika.ConnectionParameters(RABBITMQ_HOST))
        channel = connection.channel()
        channel.queue_declare(queue=PROCESSING_QUEUE, durable=True)
        channel.basic_publish(
            exchange='',
            routing_key=PROCESSING_QUEUE,
            body=json.dumps(image_info),
            properties=pika.BasicProperties(delivery_mode=2)
        )
        connection.close()

        self.status_list.addItem(f"Processing: {os.path.basename(self.image_path)} with {image_info['filter']} filter")
        self.process_button.setEnabled(False)

    def update_ui(self, data):
        stage = data['stage']
        image_info = data['data']
        
        if stage == 'processed':
            self.status_list.addItem(f"Processed image with {image_info['filter']} filter")
            self.display_processed_image(image_info)
            self.process_button.setEnabled(True)

    def display_processed_image(self, image_info):
        image_data = base64.b64decode(image_info['processed_data'])
        pixmap = QPixmap()
        pixmap.loadFromData(image_data)
        self.processed_label.setPixmap(pixmap.scaled(400, 300, Qt.KeepAspectRatio, Qt.SmoothTransformation))

    def closeEvent(self, event):
        self.worker.stop()
        self.worker.wait()
        event.accept()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())