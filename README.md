# Emmet Markup Language

Just one Emmet abbreviation is all it takes to render them all.

**Emmet Markup Language (EML)** is a made-for-fun, esoteric HTML+CSS generator built on top of [Emmet](https://emmet.io/). It uses `.ehtml` and `.ecss` files to express entire web layouts in a compact, expressive, Emmet-style syntax — now with support for multiline markup, modular components, and automatic script/style inclusion.

This project is not meant for production use. It’s an experimental playground for compressed, recursive web layout ideas — kind of like if Emmet evolved into its own language.

---

## 📁 File Types

### `.ehtml` — Emmet HTML

- Multiline Emmet syntax is supported and flattened before expansion.
- `~path/to/file;` embeds another `.ehtml` file inline (component-style).
- Transpiles into full HTML via the Emmet parser + BeautifulSoup.

#### Example:
```ehtml
html
    >(head
        >title{EML}
        +meta:vp)
    +body
        >.main
            >(~components/header;)
            +(.content
                >h1{Welcome to Emmet Markup Language})
            +(~components/footer;)
```

---

### `.ecss` — Emmet CSS

- A shorthand CSS syntax similar to Emmet.
- Abbreviated CSS properties (e.g. `pt`, `fz`, `fw`, `d`, etc.).
- Use `_` prefix for raw/unparseable CSS values.
- Automatically scoped per route and injected into the output.

#### Example:
```ecss
body > .main {
    & > .content {
        & > .title {
            pt:5rem;
            fz:2rem;
            fw:b;
        }

        & > .actions {
            d:g;
            _grid-template-columns: 1fr max-content 1fr;
        }
    }
}
```

---

## ⚙️ Transpiler Behavior

The Flask-powered transpiler:

- Serves from `src/routes/**/index.ehtml`
- Flattens and expands Emmet HTML to full HTML
- Automatically includes:
  - `style.ecss` and `script.js` from both:
    - The route directory (`src/routes/foo/`)
    - The global `src/` directory

---

## 🛠️ Project Structure

```
src/
├── components/
│   ├── header.ehtml
│   └── footer.ehtml
├── routes/
│   ├── about/
│   │   └── ...
│   ├── index.ehtml
│   ├── style.ecss      ← local style
│   └── script.js       ← local script
├── style.ecss      ← global style
└── script.js       ← global script
```

---

## 🚀 Running Locally

```bash
pip install -r requirements.txt
python main.py
```

Then open [http://localhost:5000/](http://localhost:5000/) in your browser.

---

## 🧪 Why?

because why not?