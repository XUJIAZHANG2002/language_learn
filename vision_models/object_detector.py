from transformers import AutoProcessor, OmDetTurboForObjectDetection
import torch
from PIL import Image
import numpy as np


class OmDetObjectDetector:
    """
    A clean OOP wrapper around the OmDet-Turbo text-conditioned detector.
    """

    def __init__(self, model_id="omlab/omdet-turbo-swin-tiny-hf", device=None):
        self.model_id = model_id
        self.device = device or ("cuda" if torch.cuda.is_available() else "cpu")
        
        # Load processor + model
        self.processor = AutoProcessor.from_pretrained(model_id)
        self.model = OmDetTurboForObjectDetection.from_pretrained(model_id).to(self.device)

    def detect(self, image_rgb, text_labels, threshold=0.3):
        """
        Runs detection on an RGB numpy array or PIL image.

        Returns a list of dictionaries:
            { "label": str, "score": float, "box": [x1, y1, x2, y2] }
        """
        # Ensure PIL image
        if isinstance(image_rgb, np.ndarray):
            image = Image.fromarray(image_rgb)
        else:
            image = image_rgb

        # Prepare data
        inputs = self.processor(
            images=image,
            text=text_labels,
            return_tensors="pt"
        ).to(self.device)

        # Inference
        with torch.no_grad():
            outputs = self.model(**inputs)

        # Postprocess
        results = self.processor.post_process_grounded_object_detection(
            outputs=outputs,
            threshold=threshold,
            target_sizes=[image.size[::-1]]  # (H, W)
        )[0]

        detections = []
        for score, label_idx, box in zip(results["scores"], results["labels"], results["boxes"]):
            idx = int(label_idx)
            label_text = text_labels[idx]
            detections.append({
                "label": label_text,
                "score": float(score),
                "box": box.tolist()
            })

        return detections
