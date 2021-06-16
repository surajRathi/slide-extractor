# slide-extractor

Extracts slides from video streams

- `main.py`: name
- `input.py`: wraps the various input methods (from video, from screen sharing, etc)
- `slide_check.py`: wraps the various slide similarity methods (heurestic, semantic segmentation, ocr, etc)
- `annotate_video.py`: Allows you to scroll through a video and save certain frame indices to a file
- `visualize_metrics.py`: Takes the metrics from slide checker and keyframes saved from annotate_video.py and creates a
  graph. Use pycharm sciview to save the metrics numpy array for params_grid_search.py
