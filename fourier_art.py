#!/usr/bin/env python3
"""cover.jpg -> |FFT| (log) -> palette bleu clair / rose / blanc -> resultat.png

Usage :
    python fourier_art.py cover.jpg out.png [--ref resultat.png] [--fit]
"""
import argparse
import numpy as np
from PIL import Image
from scipy.signal.windows import hann

OUT_SIZE = (4032, 3024)   # taille de resultat.png ; None = résolution native de la photo

# Palette fittée sur resultat.png : (position en log-magnitude, couleur RGB)
STOPS_POS = np.array([3.45, 8.52, 14.46])
STOPS_RGB = np.array([[46, 215, 255],     # bleu clair
                      [262, 154, 263],    # rose (>255 = saturation voulue)
                      [235, 264, 232]],   # blanc (centre / basse fréquence)
                     float)


def vignette(h, w):
    """Fenêtre de Hann 2D : bords -> 0 (noirs noirs), image 'périodique' donc plus de croix parasite."""
    return np.outer(hann(h, sym=False), hann(w, sym=False))


def log_magnitude(path, size=OUT_SIZE, window=True):  # size=(4032,3024) pour forcer
    im = Image.open(path).convert("L")
    if size and im.size != size:
        im = im.resize(size, Image.LANCZOS)
    a = np.asarray(im, np.float64)
    if window:
        a = a * vignette(*a.shape)
    F = np.fft.fftshift(np.fft.fft2(a))
    return np.log1p(np.abs(F))


def colorize(lm, pos=STOPS_POS, rgb=STOPS_RGB):
    out = np.empty(lm.shape + (3,))
    for c in range(3):
        out[..., c] = np.interp(lm, pos, rgb[:, c])
    return out


def to_png(rgb, path):
    Image.fromarray(np.clip(np.rint(rgb), 0, 255).astype(np.uint8)).save(path)


def fit_palette(lm, ref):
    """Ajuste positions + couleurs des 3 stops pour coller à l'image de référence."""
    from scipy.optimize import minimize
    idx = np.random.default_rng(0).choice(lm.size, 300_000, replace=False)
    x, y = lm.ravel()[idx], ref.reshape(-1, 3)[idx].astype(float)

    def unpack(p):
        pos = np.sort(p[:3]); rgb = p[3:].reshape(3, 3)
        return pos, rgb

    def loss(p):
        pos, rgb = unpack(p)
        if pos[0] < 3 or pos[2] > 20 or np.any(np.diff(pos) < 0.5):   # garde-fous
            return 1e9
        pred = np.stack([np.interp(x, pos, rgb[:, c]) for c in range(3)], 1)
        return np.mean(np.abs(np.clip(pred, 0, 255) - y))

    p0 = np.concatenate([STOPS_POS, STOPS_RGB.ravel()])
    r = minimize(loss, p0, method="Powell", options=dict(maxiter=4000, xtol=1e-2, ftol=1e-4))
    return unpack(r.x), r.fun


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("src"); ap.add_argument("dst")
    ap.add_argument("--ref", help="resultat.png pour mesurer l'écart")
    ap.add_argument("--no-window", action="store_true", help="désactive la vignette")
    ap.add_argument("--size", help="ex: 4032x3024 (défaut) ; 'native' pour ne pas redimensionner")
    ap.add_argument("--fit", action="store_true", help="recaler la palette sur --ref")
    a = ap.parse_args()

    size = OUT_SIZE if not a.size else (None if a.size == "native" else tuple(map(int, a.size.lower().split("x"))))
    lm = log_magnitude(a.src, size, window=not a.no_window)
    pos, rgb = STOPS_POS, STOPS_RGB
    ref = None

    
    if a.ref:
        ref = np.asarray(Image.open(a.ref).convert("RGB"))
    if a.fit and ref is not None:
        (pos, rgb), err = fit_palette(lm, ref)
        print("palette fittée :", pos.round(2).tolist(), rgb.round(0).tolist(), "MAE", round(err, 2))
    img = colorize(lm, pos, rgb)
    to_png(img, a.dst)
    if ref is not None:
        print("MAE vs ref :", np.abs(np.clip(np.rint(img), 0, 255) - ref).mean().round(2))
