import os
import cv2
import pandas as pd
from natsort import natsorted
import mediapipe as mp
import numpy as np


mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles
mp_pose = mp.solutions.pose


def get_files_paths(path, extension):
    """Функция рекурсивно ищет пути всех файлов указанного расширения(в extension) в
    директории(path) и ее поддиректориях.

    Parameters
    ----------
    path : str
        путь к директории в которой мы ищем файлы
    extension : str
        расширения файлов, которые мы ищем. Например, ".mp4"

    Returns
    -------
    list
        список путей до всех найденных файлов указанного расширения
    """
    files = []
    for dirpath, dirnames, filenames in os.walk(path):
        for filename in [f for f in filenames if f.endswith(extension)]:
            files.append(os.path.join(dirpath, filename))

    return files


class PoseEstimator:
    """Класс оценивающий ключевые точки человека.
    Использует mediapipe.solutions.pose"""

    def __init__(self, bg_color=(192, 192, 192)):
        self.bg_color = bg_color
        self.pose = mp_pose.Pose(
            static_image_mode=True,
            model_complexity=2,
            enable_segmentation=True,
            min_detection_confidence=0.5,
        )

    def predict_on_images(
        self,
        images_paths,
        input_images_dir,
        save_viz_images=False,
        draw_segmentation=False,
    ):
        pose_scheme = mp_pose.PoseLandmark

        # создаем словарь для хранения ключевых точек
        dct = {}
        dct["image_path"] = []

        if save_viz_images:
            dct["image_viz_path"] = []

        for key in pose_scheme.__members__:
            dct[f"{key}_x"] = []
            dct[f"{key}_y"] = []
            dct[f"{key}_z"] = []
            dct[f"{key}_visibility"] = []

        for image_path in images_paths:
            image, results = self.predict_on_image(image_path)
            landmarks = results.pose_landmarks

            if not landmarks:
                print(f"Ключевые точки позы не обнаружены {image_path}")
                continue

            dct["image_path"].append(image_path)
            for key in pose_scheme.__members__:
                dct[f"{key}_x"].append(landmarks.landmark[pose_scheme[key]].x)
                dct[f"{key}_y"].append(landmarks.landmark[pose_scheme[key]].y)
                dct[f"{key}_z"].append(landmarks.landmark[pose_scheme[key]].z)
                dct[f"{key}_visibility"].append(
                    landmarks.landmark[pose_scheme[key]].visibility
                )

            if save_viz_images:
                if draw_segmentation:
                    image = self.draw_segmentation(image, results.segmentation_mask)

                image = self.draw_pose_on_image(image, landmarks)

                image_path_viz = "_pose_viz".join(os.path.splitext(image_path))
                cv2.imwrite(image_path_viz, image)

                dct["image_viz_path"].append(image_path_viz)

            print(f"{image_path} обработан")

        df = pd.DataFrame.from_dict(dct)
        csv_path = os.path.join(input_images_dir, "key_points_data.csv")
        df.to_csv(csv_path, sep=";")

    def predict_on_image(self, file):
        image = cv2.imread(file)

        # Convert the BGR image to RGB before processing.
        results = self.pose.process(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))

        return image, results

    @staticmethod
    def draw_pose_on_image(image, pose_landmarks):
        # Draw pose landmarks on the image.
        mp_drawing.draw_landmarks(
            image,
            pose_landmarks,
            mp_pose.POSE_CONNECTIONS,
            landmark_drawing_spec=mp_drawing_styles.get_default_pose_landmarks_style(),
        )

        return image

    def draw_segmentation(self, image, segmentation_mask):
        annotated_image = image.copy()
        # Draw segmentation on the image.
        # To improve segmentation around boundaries, consider applying a joint
        # bilateral filter to "results.segmentation_mask" with "image".
        condition = np.stack((segmentation_mask,) * 3, axis=-1) > 0.1
        bg_image = np.zeros(image.shape, dtype=np.uint8)
        bg_image[:] = self.bg_color
        annotated_image = np.where(condition, annotated_image, bg_image)

        return annotated_image

    def close(self):
        self.pose.close()


if __name__ == "__main__":
    input_images_dir = "data_clf"
    img_ext = ".jpg"

    image_files = natsorted(get_files_paths(input_images_dir, img_ext))

    pose = PoseEstimator()
    pose.predict_on_images(
        image_files, input_images_dir, save_viz_images=True, draw_segmentation=True
    )
    pose.close()
