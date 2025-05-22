<<<<<<< HEAD
from fastapi import FastAPI, UploadFile, File, HTTPException
import numpy as np
import io
import uvicorn

app = FastAPI()

@app.post("/analyze/")
async def analyze_data(
    stroke_points_file: UploadFile = File(...)
):
    data = await stroke_points_file.read()
    pts = np.load(io.BytesIO(data))
    if pts.shape[0] < 2:
        raise HTTPException(status_code=400, detail="Not enough data points")

    xs, ys, ts = pts[:,0], pts[:,1], pts[:,2] / 1000.0

    # Split into 4 segments
    idxs = np.array_split(np.arange(len(xs)), 4)
    amplitudes, speeds = [], []
    for inds in idxs:
        if len(inds) < 2:
            amplitudes.append(0.0); speeds.append(0.0); continue
        seg_x, seg_y, seg_t = xs[inds], ys[inds], ts[inds]
        amplitudes.append(float(seg_y.max() - seg_y.min()))
        dt = np.maximum(np.diff(seg_t), 1e-3)
        v = np.hypot(np.diff(seg_x)/dt, np.diff(seg_y)/dt)
        speeds.append(float(v.mean()) if v.size else 0.0)

    # Normalized jerk
    dt_all   = np.maximum(np.diff(ts), 1e-3)
    v_all    = np.hypot(np.diff(xs)/dt_all, np.diff(ys)/dt_all)
    a_all    = np.diff(v_all) / dt_all[1:]
    jerk_all = np.diff(a_all) / dt_all[2:]
    duration = ts[-1] - ts[0]
    norm_jerk = float(np.sqrt((jerk_all**2).sum() / duration)) if duration > 0 else 0.0

    stroke_count = int(len(np.unique(pts[:,:2], axis=0)))
    diagnosis    = "PD" if any(s < 500 for s in speeds) else "Normal"

    return {
        "stroke_count": stroke_count,
        "amplitudes":   [round(a,2) for a in amplitudes],
        "speeds":       [round(s,2) for s in speeds],
        "normalized_jerk": round(norm_jerk,2),
        "diagnosis":    diagnosis
    }

if __name__ == "__main__":
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)
=======
#!/usr/bin/env python3
import sys
import math
import pygame
import numpy as np
from pathlib import Path
import matplotlib.pyplot as plt

# (TRUNCATED for brevity here, but will be complete in the actual file writing)
>>>>>>> edc411d2247aefbad33946f0d260c0347f7ad1d2
