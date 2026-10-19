# fourier_art.py

🇬🇧 [English](#english) · 🇫🇷 [Français](#français)

---

## English

### Context

This script was written to generate the artwork for the EP **[Des ordres](https://open.spotify.com/intl-fr/album/4ONY8cChg0RA4LNvRwwSp5)** by The Triper, available on all streaming platforms. The cover is a photo turned into its own Fourier spectrum.

### What it does

Turn any photo into a Fourier-spectrum artwork: the log-magnitude of its 2D FFT, recolored with a light-blue → pink → white palette.

### How it works

1. Load the photo in grayscale and resize it to 4032×3024 (the size of the reference output).
2. Apply a **vignette** (2D Hann window). Edges fade to black, so the image behaves as if it were periodic. This removes the large horizontal/vertical cross caused by the image borders and reveals the real diagonal streaks of the spectrum.
3. Compute `fftshift(fft2(image))`, then `log1p(|F|)`.
4. Rescale the values through a 3-stop palette (light blue → pink → white at the centre, i.e. the low frequencies).
5. Save as PNG.

### Requirements

```
pip install numpy pillow scipy
```

### Usage

```
python fourier_art.py cover.jpg out.png
```

The result is written to the path given as the second argument (relative to the folder you run the command from). An existing file is overwritten.

| Option | Description |
|---|---|
| `--ref resultat.png` | Reference image: prints the mean absolute error (0–255) between your output and it. |
| `--fit` | With `--ref`, re-fits the palette (stop positions and colors) to the reference. |
| `--no-window` | Disables the vignette (the border cross comes back). |
| `--size WxH` | Resize before the FFT, e.g. `--size 2576x1932`. Use `--size native` to keep the photo's own size. Default: `4032x3024`. |

### Known limitations

- The output matches the **structure** of the reference (streaks, glow, palette), not every pixel. Against the reference image, the mean error is about 22/255.
- The fine grain of the reference comes from the high frequencies of a full-resolution 4032×3024 photo. If your source is smaller and gets upscaled, those frequencies do not exist and the result is smoother. Use the full-resolution original for the closest match.

---

## Français

### Contexte

Ce script a été écrit pour générer le visuel de l'EP **[Des ordres](https://open.spotify.com/intl-fr/album/4ONY8cChg0RA4LNvRwwSp5)** de The Triper, disponible sur toutes les plateformes. La cover est une photo transformée en son propre spectre de Fourier.

### Ce que fait le script

Transforme n'importe quelle photo en œuvre issue de son spectre de Fourier : la magnitude (en log) de sa FFT 2D, recolorée avec une palette bleu clair → rose → blanc.

### Fonctionnement

1. Chargement de la photo en niveaux de gris et redimensionnement en 4032×3024 (la taille de l'image de référence).
2. Application d'une **vignette** (fenêtre de Hann 2D). Les bords tendent vers le noir, donc l'image se comporte comme si elle était périodique. Cela supprime la grande croix horizontale/verticale due aux bords de l'image et fait apparaître les vraies traînées diagonales du spectre.
3. Calcul de `fftshift(fft2(image))`, puis `log1p(|F|)`.
4. Rescaling des valeurs via une palette à 3 points (bleu clair → rose → blanc au centre, c'est-à-dire les basses fréquences).
5. Enregistrement en PNG.

### Prérequis

```
pip install numpy pillow scipy
```

### Utilisation

```
python fourier_art.py cover.jpg out.png
```

Le résultat est enregistré au chemin donné en deuxième argument (relatif au dossier où tu lances la commande). Un fichier existant est écrasé.

| Option | Description |
|---|---|
| `--ref resultat.png` | Image de référence : affiche l'erreur absolue moyenne (0–255) entre ta sortie et elle. |
| `--fit` | Avec `--ref`, recale la palette (positions et couleurs des points) sur la référence. |
| `--no-window` | Désactive la vignette (la croix des bords revient). |
| `--size LxH` | Redimensionne avant la FFT, par ex. `--size 2576x1932`. `--size native` conserve la taille de la photo. Par défaut : `4032x3024`. |

### Limites connues

- La sortie reproduit la **structure** de la référence (traînées, halo, palette), pas chaque pixel. Face à l'image de référence, l'erreur moyenne est d'environ 22/255.
- Le grain fin de la référence vient des hautes fréquences d'une photo en pleine résolution 4032×3024. Si ta source est plus petite et agrandie, ces fréquences n'existent pas et le résultat est plus lisse. Utilise l'original en pleine résolution pour t'en approcher au mieux.
