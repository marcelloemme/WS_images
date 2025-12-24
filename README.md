# 📸 E-Paper Image Upload

Upload immagini dalla galleria iPhone → Conversione automatica per display e-paper 7 colori.

## 🚀 Come funziona

1. **Carica un'immagine** nella cartella `input/` (via iPhone, web, o git)
2. **GitHub Actions** converte automaticamente l'immagine
3. **Trova il BMP** nella cartella `output/` pronto per l'e-paper

## 📱 Setup Shortcut iPhone

### Prerequisiti
- Un Personal Access Token GitHub (con permessi `repo`)
  - GitHub → Settings → Developer settings → Personal access tokens → Fine-grained tokens
  - Seleziona questa repo e dai permessi "Contents: Read and write"

### Struttura Shortcut

```
1. [Seleziona foto] - Dalla galleria

2. [Converti immagine] - In JPEG (qualità 80%)

3. [Codifica Base64] - Del risultato

4. [Testo] - Crea il JSON body:
   {
     "message": "📸 Upload da iPhone",
     "content": "[Base64]",
     "branch": "main"
   }

5. [Ottieni contenuto URL]
   URL: https://api.github.com/repos/TUO-USER/TUA-REPO/contents/input/photo_[Data corrente].jpg
   Metodo: PUT
   Headers:
     - Authorization: Bearer TUO_TOKEN
     - Content-Type: application/json
   Body: [Testo dal passo 4]

6. [Mostra notifica] - "Immagine caricata! Conversione in corso..."
```

### Shortcut Pronta (da importare)

Scarica: [epaper-upload.shortcut](./epaper-upload.shortcut) *(da creare)*

Oppure crea manualmente:

1. **Apri Comandi Rapidi** su iPhone
2. **Nuovo comando** (+)
3. Aggiungi le azioni come sopra
4. Nelle variabili:
   - `TUO_TOKEN`: il tuo Personal Access Token
   - `TUO-USER/TUA-REPO`: il path della tua repo

## 🎨 Algoritmo di Conversione

Usa l'algoritmo migliorato ispirato a [esp32-photoframe](https://github.com/aitjcize/esp32-photoframe):

- **Measured Palette**: Usa i colori reali dell'e-paper per decisioni migliori durante il dithering
- **Floyd-Steinberg Dithering**: Diffusione dell'errore per transizioni colore più naturali
- **Saturation Boost**: Compensa i colori slavati dell'e-paper

### Palette 7 Colori (Waveshare E6)
| Indice | Colore | RGB |
|--------|--------|-----|
| 0 | Nero | 0, 0, 0 |
| 1 | Bianco | 255, 255, 255 |
| 2 | Verde | 0, 128, 0 |
| 3 | Blu | 0, 0, 255 |
| 4 | Rosso | 255, 0, 0 |
| 5 | Giallo | 255, 255, 0 |
| 6 | Arancione | 255, 128, 0 |

## 📁 Struttura Repository

```
├── input/           ← Carica qui le immagini
├── output/          ← BMP convertiti (auto-generati)
├── convert_for_epaper.py
├── .github/workflows/convert.yml
└── README.md
```

## 🔧 Conversione Locale

```bash
# Installa dipendenze
pip install pillow numpy

# Converti un'immagine
python convert_for_epaper.py foto.jpg output.bmp
```

## ⚙️ Personalizzazione

Nel file `convert_for_epaper.py` puoi modificare:

```python
# Saturazione (1.0 = normale, 1.5 = consigliato per e-paper)
saturation=1.5

# Dimensioni (800x480 per Waveshare 7.3")
width=800, height=480
```

## 📋 Troubleshooting

**L'azione non parte?**
- Verifica che l'immagine sia in `input/`
- Controlla i permessi del token

**Colori sbiaditi?**
- Aumenta `saturation` nel converter (prova 1.8 o 2.0)

**Immagine troppo scura/chiara?**
- Usa la versione completa `epaper_converter.py` con parametri `--exposure` e `--scurve`

## 📚 Risorse

- [esp32-photoframe](https://github.com/aitjcize/esp32-photoframe) - Firmware con algoritmo originale
- [Waveshare E6 Wiki](https://www.waveshare.com/wiki/7.3inch_e-Paper_HAT_(E)_Manual)
- [Floyd-Steinberg Dithering](https://en.wikipedia.org/wiki/Floyd%E2%80%93Steinberg_dithering)
