"""ChatGPT 손폰 사진의 말풍선·이름·시간 글씨를 전부 다시 씀.
말풍선마다 따로 원근 변환(렌더 말풍선 4모서리 → 사진 말풍선 4모서리)을 구해, 그 말풍선 글씨와 옆 시간·위 이름을 옮겨 씀.
사진의 기존 글씨는 inpaint로 지우고, 새 글씨는 사진 바탕색을 어둡게 한 색으로 얹음(색조·금·반사 유지)."""
import numpy as np, cv2
from PIL import Image
P = np.array(Image.open("src/chatgpt_photo.png").convert("RGB"))
R = np.array(Image.open("out/kakao_screen.png").convert("RGB"))
Pi, Ri = P.astype(int), R.astype(int)
h, w = P.shape[:2]

def bubble_quad(mask, seed):
    m = cv2.morphologyEx(mask.astype(np.uint8), cv2.MORPH_CLOSE, np.ones((15, 15), np.uint8))
    m = cv2.morphologyEx(m, cv2.MORPH_OPEN, np.ones((5, 5), np.uint8))
    n, lab, st, _ = cv2.connectedComponentsWithStats(m)
    def dist(j):
        x, y, ww, hh, ar = st[j]
        if ar < 1500: return 1e9
        dx = max(x - seed[0], 0, seed[0] - (x + ww)); dy = max(y - seed[1], 0, seed[1] - (y + hh))
        return dx + dy
    i = min(range(1, n), key=dist)
    cnt, _ = cv2.findContours((lab == i).astype(np.uint8), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    c = max(cnt, key=cv2.contourArea)
    box = cv2.boxPoints(cv2.minAreaRect(c))
    s = box.sum(1); d = box[:, 1] - box[:, 0]
    return np.array([box[s.argmin()], box[d.argmin()], box[s.argmax()], box[d.argmax()]], np.float32), (lab == i)

pw = (Pi[..., 0] > 185) & (Pi[..., 2] > 190) & (Pi[..., 0] - Pi[..., 2] > -30)
py = (Pi[..., 0] > 170) & (Pi[..., 2] < 140)
py0 = py.copy(); py0[:186] = False
rw = (Ri[..., 0] > 250) & (Ri[..., 1] > 250)
ry = (Ri[..., 2] < 150) & (Ri[..., 0] > 230)
ry[:405] = False  # 잘린 위쪽 노란 띠 제외
# (렌더 마스크, 렌더 씨앗, 사진 마스크, 사진 씨앗, 옆으로 넓힐 방향)
B = [
    (ry, (900, 450), py0, (645, 225), "none"),
    (rw, (180, 640), pw, (340, 345), "right"),
    (rw, (180, 1300), pw, (360, 700), "right"),
    (ry, (1060, 1900), py, (905, 1025), "none"),
    (ry, (1000, 2010), py, (880, 1100), "left"),
    (rw, (180, 2200), pw, (450, 1225), "right"),
]
Rl = R.astype(np.float32).mean(2)
Rbg = np.maximum(cv2.medianBlur(R, 41).astype(np.float32).mean(2), Rl)
alpha_r = np.clip((Rbg - Rl) / np.maximum(Rbg - 25, 1), 0, 1)
alpha_r[380:520, :690] = 0  # 첫 노란 말풍선 옆 시간은 사진 것 유지
Pl = P.astype(np.float32).mean(2)
Pbg = cv2.medianBlur(P, 31).astype(np.float32).mean(2)
AW = np.zeros((h, w), np.float32); ER = np.zeros((h, w), np.uint8)
dbg = P.copy()
for rm, rs, pm, ps, side in B:
    rq, rmask = bubble_quad(rm, rs)
    pq, pmask = bubble_quad(pm, ps)
    Hm = cv2.getPerspectiveTransform(rq, pq)
    x0, y0 = rq[:, 0].min(), rq[:, 1].min(); x1, y1 = rq[:, 0].max(), rq[:, 1].max()
    # 렌더 영역: 말풍선 + 옆 시간(160px) + 위 이름(흰 말풍선, 첫 줄만)
    reg = np.zeros(Rl.shape, np.uint8)
    ex0 = x0 - (175 if side == "left" else 0); ex1 = x1 + (175 if side == "right" else 0)
    ey0 = y0 - (58 if side == "right" else 0)
    cv2.rectangle(reg, (int(ex0), int(ey0)), (int(ex1), int(y1) + 4), 1, -1)
    reg[:, :160] = 0
    a = cv2.warpPerspective(alpha_r * reg, Hm, (w, h), flags=cv2.INTER_AREA)
    AW = np.maximum(AW, a)
    preg = cv2.warpPerspective(reg.astype(np.float32), Hm, (w, h)) > 0.5
    old = ((Pbg - Pl) > 28) & preg
    ER |= (cv2.dilate(old.astype(np.uint8), np.ones((5, 5), np.uint8)) & preg.astype(np.uint8))
    cv2.polylines(dbg, [np.int32(pq)], True, (255, 0, 0), 2)
    cv2.polylines(dbg, [np.int32(cv2.perspectiveTransform(rq[None], Hm)[0])], True, (0, 200, 0), 1)
ER |= (cv2.dilate((AW > 0.08).astype(np.uint8), np.ones((5, 5), np.uint8)))
bg = cv2.inpaint(P, ER * 255, 5, cv2.INPAINT_TELEA).astype(np.float32)
a = cv2.GaussianBlur(AW, (0, 0), 0.55)[..., None]
out = bg * (1 - a) + (bg * 0.2) * a
out += np.random.default_rng(3).normal(0, 2.0, out.shape) * (ER[..., None] > 0)
O = Image.fromarray(np.clip(out, 0, 255).astype(np.uint8)); O.save("out/01_chatgpt_fixed.png")
O.crop((200, 120, 1000, 700)).save("/tmp/r1.png"); O.crop((200, 650, 1050, 1300)).save("/tmp/r2.png")
Image.fromarray(dbg).resize((543, 724)).save("/tmp/dbg.png")
