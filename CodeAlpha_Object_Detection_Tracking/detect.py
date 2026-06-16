"""
╔══════════════════════════════════════════════════════════╗
║   CodeAlpha — Task 4: Object Detection & Tracking        ║
║   Model  : YOLOv8 (Ultralytics)                          ║
║   Tracker: ByteTrack (built-in)                          ║
║   Input  : Webcam (default) or any video file            ║
╚══════════════════════════════════════════════════════════╝
"""

import cv2
import time
import argparse
import random
from collections import defaultdict
from ultralytics import YOLO

# ─────────────────────────────────────────────
#  CONFIG
# ─────────────────────────────────────────────
MODEL_PATH   = "yolov8s.pt"   # nano = fastest; swap to yolov8s.pt for better accuracy
CONF_THRESH  = 0.40           # minimum confidence to show a detection
IOU_THRESH   = 0.45           # NMS IOU threshold
FONT         = cv2.FONT_HERSHEY_SIMPLEX


def get_color(class_id: int) -> tuple:
    """Return a consistent BGR color for each class id."""
    random.seed(class_id * 42)
    return (random.randint(50, 255), random.randint(50, 255), random.randint(50, 255))


def draw_box(frame, x1, y1, x2, y2, label: str, color: tuple):
    """Draw a rounded-style bounding box with a filled label badge."""
    thickness = 2

    # Bounding box
    cv2.rectangle(frame, (x1, y1), (x2, y2), color, thickness)

    # Label badge background
    (tw, th), baseline = cv2.getTextSize(label, FONT, 0.55, 1)
    badge_y1 = max(y1 - th - baseline - 6, 0)
    badge_y2 = y1
    cv2.rectangle(frame, (x1, badge_y1), (x1 + tw + 8, badge_y2), color, -1)

    # Label text
    cv2.putText(frame, label, (x1 + 4, y1 - baseline - 2),
                FONT, 0.55, (255, 255, 255), 1, cv2.LINE_AA)


def draw_hud(frame, fps: float, counts: dict, total_tracked: int):
    """Draw the top-left HUD overlay with FPS, count, class breakdown."""
    h, w = frame.shape[:2]

    # Semi-transparent dark panel
    overlay = frame.copy()
    panel_h = 40 + len(counts) * 22 + 10
    cv2.rectangle(overlay, (10, 10), (220, panel_h), (20, 20, 20), -1)
    cv2.addWeighted(overlay, 0.6, frame, 0.4, 0, frame)

    # FPS
    cv2.putText(frame, f"FPS : {fps:.1f}", (18, 32),
                FONT, 0.55, (0, 255, 180), 1, cv2.LINE_AA)

    # Total objects
    cv2.putText(frame, f"Objects : {total_tracked}", (18, 52),
                FONT, 0.55, (0, 200, 255), 1, cv2.LINE_AA)

    # Per-class breakdown
    y = 72
    for cls_name, cnt in sorted(counts.items()):
        cv2.putText(frame, f"  {cls_name}: {cnt}", (18, y),
                    FONT, 0.48, (200, 200, 200), 1, cv2.LINE_AA)
        y += 22

    # Bottom-right watermark
    label = "CodeAlpha | YOLOv8 + ByteTrack"
    (tw, _), _ = cv2.getTextSize(label, FONT, 0.42, 1)
    cv2.putText(frame, label, (w - tw - 10, h - 10),
                FONT, 0.42, (100, 100, 100), 1, cv2.LINE_AA)


def run(source, show_conf: bool):
    """Main detection + tracking loop."""

    # Load model (downloads yolov8n.pt on first run, ~6 MB)
    print(f"\n[INFO] Loading model: {MODEL_PATH}")
    model = YOLO(MODEL_PATH)
    class_names = model.names
    print(f"[INFO] Model loaded — {len(class_names)} classes")
    print(f"[INFO] Source: {'Webcam (0)' if source == 0 else source}")
    print("[INFO] Press  Q  to quit\n")

    cap = cv2.VideoCapture(source)
    if not cap.isOpened():
        print("[ERROR] Cannot open video source. Check your webcam or file path.")
        return

    prev_time = time.time()

    while True:
        ret, frame = cap.read()
        if not ret:
            print("[INFO] Stream ended.")
            break

        # ── Run YOLOv8 with ByteTrack ──────────────────────────
        results = model.track(
            frame,
            conf=CONF_THRESH,
            iou=IOU_THRESH,
            tracker="bytetrack.yaml",
            persist=True,       # keep track IDs between frames
            verbose=False
        )

        counts = defaultdict(int)
        total  = 0

        if results[0].boxes is not None:
            boxes = results[0].boxes

            for box in boxes:
                # Coordinates
                x1, y1, x2, y2 = map(int, box.xyxy[0].tolist())

                # Class info
                cls_id   = int(box.cls[0])
                cls_name = class_names[cls_id]
                conf     = float(box.conf[0])

                # Track ID (may be None on first frame)
                track_id = int(box.id[0]) if box.id is not None else -1

                color = get_color(cls_id)

                # Build label string
                id_str   = f"ID:{track_id} " if track_id != -1 else ""
                conf_str = f" {conf:.0%}" if show_conf else ""
                label    = f"{id_str}{cls_name}{conf_str}"

                draw_box(frame, x1, y1, x2, y2, label, color)

                counts[cls_name] += 1
                total += 1

        # ── FPS ───────────────────────────────────────────────
        now  = time.time()
        fps  = 1.0 / (now - prev_time + 1e-6)
        prev_time = now

        # ── HUD ───────────────────────────────────────────────
        draw_hud(frame, fps, dict(counts), total)

        cv2.imshow("CodeAlpha — Object Detection & Tracking", frame)

        if cv2.waitKey(1) & 0xFF == ord("q"):
            print("[INFO] Quit requested by user.")
            break

    cap.release()
    cv2.destroyAllWindows()
    print("[INFO] Done.")


# ─────────────────────────────────────────────
#  ENTRY POINT
# ─────────────────────────────────────────────
if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="YOLOv8 + ByteTrack — Real-time Object Detection & Tracking"
    )
    parser.add_argument(
        "--source",
        default="0",
        help="Video source: 0 for webcam, or path to a video file (e.g. video.mp4)"
    )
    parser.add_argument(
        "--show-conf",
        action="store_true",
        help="Show confidence score on each bounding box label"
    )
    args = parser.parse_args()

    # Auto-convert "0" string → int for webcam
    source = int(args.source) if args.source.isdigit() else args.source

    run(source, args.show_conf)
