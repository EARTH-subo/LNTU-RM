import sys
import os
import cv2
from PySide6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, 
                               QHBoxLayout, QPushButton, QLabel, QLineEdit, 
                               QFileDialog, QSpinBox, QProgressBar, QMessageBox,
                               QGroupBox)
from PySide6.QtCore import Qt, QThread, Signal
from PySide6.QtGui import QFont


class VideoCaptureThread(QThread):
    progress = Signal(int)
    finished = Signal(str, int)
    error = Signal(str)

    def __init__(self, video_path, output_dir, num_frames):
        super().__init__()
        self.video_path = video_path
        self.output_dir = output_dir
        self.num_frames = num_frames

    def run(self):
        try:
            cap = cv2.VideoCapture(self.video_path)
            if not cap.isOpened():
                self.error.emit("无法打开视频文件")
                return

            total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
            fps = cap.get(cv2.CAP_PROP_FPS)

            if total_frames <= 0:
                self.error.emit("无法获取视频帧数")
                cap.release()
                return

            # 计算需要截取的帧间隔
            if self.num_frames >= total_frames:
                frame_indices = list(range(total_frames))
            else:
                interval = total_frames / self.num_frames
                frame_indices = [int(i * interval) for i in range(self.num_frames)]

            saved_count = 0
            for idx, frame_idx in enumerate(frame_indices):
                cap.set(cv2.CAP_PROP_POS_FRAMES, frame_idx)
                ret, frame = cap.read()
                
                if ret:
                    # 保存图片
                    filename = f"frame_{saved_count + 1:06d}.jpg"
                    filepath = os.path.join(self.output_dir, filename)
                    cv2.imwrite(filepath, frame)
                    saved_count += 1
                
                # 更新进度
                progress = int((idx + 1) / len(frame_indices) * 100)
                self.progress.emit(progress)

            cap.release()
            self.finished.emit(self.output_dir, saved_count)

        except Exception as e:
            self.error.emit(f"处理出错: {str(e)}")


class VideoScreenshotTool(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("视频截图工具")
        self.setMinimumSize(600, 450)
        
        self.video_path = ""
        self.output_dir = ""
        self.capture_thread = None
        
        self.setup_ui()

    def setup_ui(self):
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        layout = QVBoxLayout(central_widget)
        layout.setSpacing(20)
        layout.setContentsMargins(30, 30, 30, 30)

        # 标题
        title_label = QLabel("视频截图工具")
        title_label.setFont(QFont("Arial", 18, QFont.Bold))
        title_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(title_label)

        # 视频选择区域
        video_group = QGroupBox("视频文件")
        video_layout = QVBoxLayout()
        
        video_file_layout = QHBoxLayout()
        self.video_path_edit = QLineEdit()
        self.video_path_edit.setReadOnly(True)
        self.video_path_edit.setPlaceholderText("请选择视频文件")
        video_select_btn = QPushButton("选择视频")
        video_select_btn.clicked.connect(self.select_video)
        video_file_layout.addWidget(self.video_path_edit)
        video_file_layout.addWidget(video_select_btn)
        
        video_layout.addLayout(video_file_layout)
        video_group.setLayout(video_layout)
        layout.addWidget(video_group)

        # 输出设置区域
        output_group = QGroupBox("输出设置")
        output_layout = QVBoxLayout()
        
        # 帧数设置
        frame_layout = QHBoxLayout()
        frame_label = QLabel("截取图片数量:")
        self.frame_spinbox = QSpinBox()
        self.frame_spinbox.setMinimum(1)
        self.frame_spinbox.setMaximum(10000)
        self.frame_spinbox.setValue(100)
        self.frame_spinbox.setSuffix(" 张")
        frame_layout.addWidget(frame_label)
        frame_layout.addWidget(self.frame_spinbox)
        frame_layout.addStretch()
        
        output_layout.addLayout(frame_layout)
        output_group.setLayout(output_layout)
        layout.addWidget(output_group)

        # 操作按钮
        btn_layout = QHBoxLayout()
        self.start_btn = QPushButton("开始截取")
        self.start_btn.setMinimumHeight(45)
        self.start_btn.clicked.connect(self.start_capture)
        self.start_btn.setEnabled(False)
        btn_layout.addWidget(self.start_btn)
        layout.addLayout(btn_layout)

        # 进度条
        self.progress_bar = QProgressBar()
        self.progress_bar.setVisible(False)
        layout.addWidget(self.progress_bar)

        # 状态标签
        self.status_label = QLabel("就绪")
        self.status_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.status_label)

        layout.addStretch()

    def select_video(self):
        file_path, _ = QFileDialog.getOpenFileName(
            self,
            "选择视频文件",
            "",
            "视频文件 (*.mp4 *.avi *.mov *.mkv *.flv *.wmv);;所有文件 (*.*)"
        )
        
        if file_path:
            self.video_path = file_path
            self.video_path_edit.setText(file_path)
            self.start_btn.setEnabled(True)
            self.status_label.setText("已选择视频文件")

    def get_unique_output_dir(self):
        base_dir = os.path.join(os.path.dirname(__file__), "pic")
        counter = 1
        
        output_dir = base_dir
        while os.path.exists(output_dir):
            output_dir = f"{base_dir}_{counter}"
            counter += 1
        
        os.makedirs(output_dir, exist_ok=True)
        return output_dir

    def start_capture(self):
        if not self.video_path:
            QMessageBox.warning(self, "警告", "请先选择视频文件")
            return

        num_frames = self.frame_spinbox.value()
        
        # 获取输出目录
        self.output_dir = self.get_unique_output_dir()
        
        # 禁用按钮
        self.start_btn.setEnabled(False)
        self.progress_bar.setVisible(True)
        self.progress_bar.setValue(0)
        self.status_label.setText("正在处理...")

        # 启动处理线程
        self.capture_thread = VideoCaptureThread(self.video_path, self.output_dir, num_frames)
        self.capture_thread.progress.connect(self.update_progress)
        self.capture_thread.finished.connect(self.capture_finished)
        self.capture_thread.error.connect(self.capture_error)
        self.capture_thread.start()

    def update_progress(self, value):
        self.progress_bar.setValue(value)

    def capture_finished(self, output_dir, count):
        self.start_btn.setEnabled(True)
        self.status_label.setText(f"完成！已保存 {count} 张图片到: {output_dir}")
        QMessageBox.information(
            self,
            "完成",
            f"成功截取 {count} 张图片！\n保存目录: {output_dir}"
        )

    def capture_error(self, error_msg):
        self.start_btn.setEnabled(True)
        self.progress_bar.setVisible(False)
        self.status_label.setText(f"出错: {error_msg}")
        QMessageBox.critical(self, "错误", error_msg)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    
    # 设置应用样式
    app.setStyle("Fusion")
    
    window = VideoScreenshotTool()
    window.show()
    
    sys.exit(app.exec())