# Efficient Page Replacement Algorithm Simulator
### CSE316 — Operating Systems | CA-2 Project | LPU

---

## 📌 Project Overview
A Python-based GUI simulator that allows users to test and compare **FIFO**, **LRU**, and **Optimal** page replacement algorithms. It visualizes frame states step-by-step and provides detailed performance metrics.

---

## 👥 Group Members
| Name | Roll Number |
|------|------------|
| Saurav Kumar | R2E048B55 |
| Narayana Gopi | R2E048B56 |

---

## 🧠 Algorithms Implemented
| Algorithm | Description |
|-----------|-------------|
| **FIFO** | Replaces the page that has been in memory the longest |
| **LRU** | Replaces the page that was least recently used |
| **Optimal** | Replaces the page that won't be used for the longest future time |

---

## 🗂 Project Structure
```
page_replacement_simulator/
│
├── main.py          # Tkinter GUI — all UI components
├── algorithms.py    # Core logic for FIFO, LRU, Optimal
└── README.md        # Project documentation
```

---

## ⚙ Tech Stack
- **Language:** Python 3.10+
- **GUI:** Tkinter (built-in)
- **Charts:** Matplotlib + FigureCanvasTkAgg
- **Version Control:** Git / GitHub

---

## 🚀 How to Run

### 1. Install Dependencies
```bash
pip install matplotlib
```

### 2. Run the App
```bash
python main.py
```

---

## 🖥 Features
- Input custom page reference string and number of frames (2–5)
- Select one or all algorithms to compare
- **Tab 1** — Step-by-step color-coded frame state table (green = hit, red = fault)
- **Tab 2** — Bar charts comparing page faults and hit rates
- **Tab 3** — Summary cards with metrics + best algorithm highlight

---

## 📊 Performance Metrics Shown
- Total Page Faults
- Total Page Hits
- Hit Rate (%)
- Miss Rate (%)
- Best-performing algorithm (auto-highlighted)

---

## 📁 Module Breakdown
| Module | File | Responsibility |
|--------|------|----------------|
| Logic Engine | `algorithms.py` | FIFO, LRU, Optimal implementations |
| Visualization | `main.py` (render methods) | Frame table, bar charts |
| Interface | `main.py` (build methods) | Input panel, tabs, controls |

---

## 🔮 Future Scope
- Add LFU (Least Frequently Used) and MRU algorithms
- Export simulation results as PDF/CSV
- Animate page replacement frame-by-frame
- Add a dark/light theme toggle
