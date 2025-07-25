
## Install

```bash
pip install -r requirements.txt
python -m spacy download en_core_web_sm
```

## use
```bash
python pattern_finder.py <フォルダパス> [--level レベル]
```

eg：
```bash
python pattern_finder.py texts

python pattern_finder.py texts --level 2

python pattern_finder.py texts --level 3

python pattern_finder.py texts --level 4
```