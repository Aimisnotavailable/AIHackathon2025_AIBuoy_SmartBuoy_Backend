import cv2
import argparse
import time
from ultralytics import YOLO
import json

def parse_args():
    """
    Parse command-line arguments for model, thresholds, and input source.
    """
    parser = argparse.ArgumentParser(description="Real-Time YOLO (Ultralytics) Object Detection")

    # Model and inference parameters
    parser.add_argument(
        "--model", type=str, default="best.pt",
        help="Path to Ultralytics YOLO model file (.pt)"
    )
    parser.add_argument(
        "--conf-thres", type=float, default=0.25,
        help="Confidence threshold for detections"
    )
    parser.add_argument(
        "--iou-thres", type=float, default=0.45,
        help="IOU threshold for non-maximum suppression"
    )
    parser.add_argument(
        "--source", type=str, default="0",
        help="Video source: '0' for webcam or path to video file"
    )

    return parser.parse_args()

def annotate_frame(frame, boxes, confidences, class_ids, names):
    """
    Draw bounding boxes, class labels, and confidence scores on the frame.
    """
    for box, conf, cls in zip(boxes, confidences, class_ids):
        x1, y1, x2, y2 = box
        label = f"{names[int(cls)]}: {conf:.2f}"
        color = (0, 255, 0)

        cv2.rectangle(frame, (x1, y1), (x2, y2), color, 2)
        cv2.putText(
            frame, label, (x1, y1 - 10),
            cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 2
        )
    return frame

def dump(data):

    with open("dump.txt", "w+") as fp:
        fp.write(str(data.orig_img))
    return

def main():
    args = parse_args()

    # Load Ultralytics YOLO model
    model = YOLO(args.model)

    # Prepare video source (webcam or file)
    source = 0 if args.source == "0" else args.source
    cap = cv2.VideoCapture(source)
    if not cap.isOpened():
        print(f"Error: Cannot open video source {args.source}")
        return

    print("Press 'q' to quit.")

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        # Inference: returns a list of Results, take the first (batch size = 1)
        start_time = time.time()
        results = model(
            frame,
            conf=args.conf_thres,
            iou=args.iou_thres,
            device="cuda",        # change to "cuda" if GPU is available
            stream=False         # we process frame-by-frame
        )[0]

        dump(results)
        elapsed = time.time() - start_time

        # Extract boxes, confidences, class IDs
        boxes = results.boxes.xyxy.cpu().numpy().astype(int)  # [N, 4]
        confidences = results.boxes.conf.cpu().numpy()       # [N]
        class_ids = results.boxes.cls.cpu().numpy()          # [N]

        # Annotate and display FPS
        annotated = annotate_frame(
            frame, boxes, confidences, class_ids, model.names
        )

        fps = 1 / elapsed if elapsed > 0 else 0
        cv2.putText(
            annotated, f"FPS: {fps:.1f}", (15, 25),
            cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 255), 2
        )

        cv2.imshow("Ultralytics YOLO Detection", annotated)

        # Exit loop on 'q'
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # Cleanup
    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
