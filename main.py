import cv2
import numpy as np
from scipy.spatial import ConvexHull, Delaunay
from shapely.geometry import MultiPoint, LineString, MultiLineString
from shapely.ops import unary_union, polygonize
from PIL import Image
import matplotlib.pyplot as plt

# ตัวอย่างจุด
points = np.array([
    [150, 200], [160, 220], [170, 210], [180, 230], [190, 250],
    [200, 240], [210, 220], [220, 200], [230, 190], [240, 210]
])

# กำหนดพื้นหลังเป็นภาพเปล่า
frame = np.ones((400, 600, 3), dtype=np.uint8) * 255

# ฟังก์ชันวาด convex hull
def draw_convex_hull(img, pts, color, fill_alpha=0.2):
    if len(pts) >= 3:
        hull = ConvexHull(pts)
        hull_pts = pts[hull.vertices]
        overlay = img.copy()
        cv2.fillPoly(overlay, [hull_pts], color)
        return cv2.addWeighted(overlay, fill_alpha, img, 1 - fill_alpha, 0)
    return img

# ฟังก์ชันสร้าง concave hull
def alpha_shape(points, alpha):
    if len(points) < 4:
        return MultiPoint(points).convex_hull

    tri = Delaunay(points)
    edges = set()
    edge_points = []

    for ia, ib, ic in tri.simplices:
        pa, pb, pc = points[ia], points[ib], points[ic]
        a, b, c = np.linalg.norm(pb - pa), np.linalg.norm(pc - pb), np.linalg.norm(pa - pc)
        s = (a + b + c) / 2.0
        area = np.sqrt(max(s * (s - a) * (s - b) * (s - c), 0))
        if area == 0:
            continue
        circum_r = a * b * c / (4.0 * area)
        if circum_r < 1.0 / alpha:
            edges.update([(ia, ib), (ib, ic), (ic, ia)])

    for i, j in edges:
        edge_points.append(LineString([points[i], points[j]]))

    mls = MultiLineString(edge_points)
    return unary_union(list(polygonize(mls)))  # ✅ แก้ไขตรงนี้

# วาดจุด gaze
for (x, y) in points:
    cv2.circle(frame, (x, y), 6, (0, 0, 255), -1)

# วาด convex hull สีน้ำเงิน
frame = draw_convex_hull(frame, points, color=(255, 0, 0), fill_alpha=0.2)

# วาด concave hull สีแดง
concave = alpha_shape(points, alpha=0.03)
if concave.geom_type == 'Polygon':
    coords = np.array(concave.exterior.coords).astype(np.int32)
    overlay = frame.copy()
    cv2.fillPoly(overlay, [coords], color=(0, 0, 255))
    frame = cv2.addWeighted(overlay, 0.2, frame, 0.8, 0)

# แสดงผล
img_pil = Image.fromarray(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
plt.figure(figsize=(10, 6))
plt.imshow(img_pil)
plt.axis('off')
plt.title("🔵 Convex (Blue) | 🔴 Concave (Red)")
plt.tight_layout()
plt.show()
