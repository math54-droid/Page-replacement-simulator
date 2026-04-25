# GUI layout built
import tkinter as tk
from tkinter import ttk, messagebox
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import matplotlib.patches as mpatches

from algorithms import fifo, lru, optimal

BG_DARK     = "#1e1e2e"
BG_PANEL    = "#2a2a3e"
BG_CARD     = "#313149"
ACCENT      = "#7c6af7"
ACCENT2     = "#f7786a"
ACCENT3     = "#56c9a4"
TEXT_LIGHT  = "#e0e0f0"
TEXT_DIM    = "#8888aa"
HIT_COLOR   = "#56c9a4"
FAULT_COLOR = "#f7786a"
EMPTY_COLOR = "#3a3a55"
HEADER_COLOR= "#7c6af7"

FONT_TITLE  = ("Segoe UI", 18, "bold")
FONT_HEADER = ("Segoe UI", 11, "bold")
FONT_BODY   = ("Segoe UI", 10)
FONT_MONO   = ("Courier New", 10)
FONT_SMALL  = ("Segoe UI", 9)


class PageReplacementSimulator(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Page Replacement Algorithm Simulator — CSE316")
        self.geometry("1200x800")
        self.minsize(1000, 700)
        self.configure(bg=BG_DARK)
        self.resizable(True, True)

        self._build_ui()

    
    def _build_ui(self):
        # Title bar
        title_bar = tk.Frame(self, bg=ACCENT, height=52)
        title_bar.pack(fill="x")
        title_bar.pack_propagate(False)
        tk.Label(title_bar, text="⚙  Page Replacement Algorithm Simulator",
                 font=FONT_TITLE, bg=ACCENT, fg="white").pack(side="left", padx=20, pady=10)
        tk.Label(title_bar, text="CSE316 | Operating Systems",
                 font=FONT_SMALL, bg=ACCENT, fg="#d0ccff").pack(side="right", padx=20)

        
        main = tk.Frame(self, bg=BG_DARK)
        main.pack(fill="both", expand=True, padx=14, pady=10)

        
        left = tk.Frame(main, bg=BG_PANEL, width=280, relief="flat", bd=0)
        left.pack(side="left", fill="y", padx=(0, 10))
        left.pack_propagate(False)
        self._build_input_panel(left)

        
        right = tk.Frame(main, bg=BG_DARK)
        right.pack(side="left", fill="both", expand=True)
        self._build_output_panel(right)

    def _section(self, parent, text):
        tk.Label(parent, text=text, font=FONT_HEADER,
                 bg=BG_PANEL, fg=ACCENT).pack(anchor="w", padx=16, pady=(14, 4))

    def _build_input_panel(self, parent):
        tk.Label(parent, text="Configuration", font=("Segoe UI", 13, "bold"),
                 bg=BG_PANEL, fg=TEXT_LIGHT).pack(anchor="w", padx=16, pady=(16, 2))
        ttk.Separator(parent).pack(fill="x", padx=12, pady=4)

    
        self._section(parent, "📄 Reference String")
        tk.Label(parent, text="Enter page numbers (space-separated):",
                 font=FONT_SMALL, bg=BG_PANEL, fg=TEXT_DIM, wraplength=240).pack(anchor="w", padx=16)
        self.ref_var = tk.StringVar(value="7 0 1 2 0 3 0 4 2 3 0 3 2 1 2 0 1 7 0 1")
        ref_entry = tk.Entry(parent, textvariable=self.ref_var, font=FONT_MONO,
                             bg=BG_CARD, fg=TEXT_LIGHT, insertbackground=TEXT_LIGHT,
                             relief="flat", bd=0, highlightthickness=1,
                             highlightcolor=ACCENT, highlightbackground=BG_CARD)
        ref_entry.pack(fill="x", padx=16, pady=(4, 8), ipady=6)

        
        self._section(parent, "🖼  Number of Frames")
        frame_row = tk.Frame(parent, bg=BG_PANEL)
        frame_row.pack(fill="x", padx=16)
        self.frame_var = tk.IntVar(value=3)
        for n in [2, 3, 4, 5]:
            rb = tk.Radiobutton(frame_row, text=str(n), variable=self.frame_var, value=n,
                                bg=BG_PANEL, fg=TEXT_LIGHT, selectcolor=ACCENT,
                                activebackground=BG_PANEL, font=FONT_BODY)
            rb.pack(side="left", padx=6)

    
        self._section(parent, "🧠 Algorithm")
        self.algo_var = tk.StringVar(value="All")
        for algo in ["All", "FIFO", "LRU", "Optimal"]:
            rb = tk.Radiobutton(parent, text=algo, variable=self.algo_var, value=algo,
                                bg=BG_PANEL, fg=TEXT_LIGHT, selectcolor=ACCENT,
                                activebackground=BG_PANEL, font=FONT_BODY)
            rb.pack(anchor="w", padx=28)

        ttk.Separator(parent).pack(fill="x", padx=12, pady=14)

        
        run_btn = tk.Button(parent, text="▶  RUN SIMULATION", font=("Segoe UI", 11, "bold"),
                            bg=ACCENT, fg="white", relief="flat", bd=0,
                            activebackground="#6a58e0", activeforeground="white",
                            cursor="hand2", command=self.run_simulation)
        run_btn.pack(fill="x", padx=16, ipady=10)

    
        reset_btn = tk.Button(parent, text="↺  Reset", font=FONT_SMALL,
                              bg=BG_CARD, fg=TEXT_DIM, relief="flat", bd=0,
                              activebackground=BG_CARD, cursor="hand2",
                              command=self.reset)
        reset_btn.pack(fill="x", padx=16, pady=(6, 0), ipady=6)

        ttk.Separator(parent).pack(fill="x", padx=12, pady=14)

        
        tk.Label(parent, text="Legend", font=FONT_HEADER, bg=BG_PANEL, fg=TEXT_DIM).pack(anchor="w", padx=16)
        for color, label in [(HIT_COLOR, "Page Hit"), (FAULT_COLOR, "Page Fault"), (EMPTY_COLOR, "Empty Frame")]:
            row = tk.Frame(parent, bg=BG_PANEL)
            row.pack(anchor="w", padx=20, pady=2)
            tk.Label(row, bg=color, width=2, relief="flat").pack(side="left", padx=(0, 8))
            tk.Label(row, text=label, font=FONT_SMALL, bg=BG_PANEL, fg=TEXT_DIM).pack(side="left")

    def _build_output_panel(self, parent):
        style = ttk.Style()
        style.theme_use("clam")
        style.configure("TNotebook", background=BG_DARK, borderwidth=0)
        style.configure("TNotebook.Tab", background=BG_PANEL, foreground=TEXT_DIM,
                        font=FONT_HEADER, padding=[14, 6])
        style.map("TNotebook.Tab", background=[("selected", ACCENT)],
                  foreground=[("selected", "white")])

        self.notebook = ttk.Notebook(parent)
        self.notebook.pack(fill="both", expand=True)

        
        self.tab_table = tk.Frame(self.notebook, bg=BG_DARK)
        self.notebook.add(self.tab_table, text="  📋 Step-by-Step Table  ")

        
        self.tab_chart = tk.Frame(self.notebook, bg=BG_DARK)
        self.notebook.add(self.tab_chart, text="  📊 Performance Chart  ")

        
        self.tab_summary = tk.Frame(self.notebook, bg=BG_DARK)
        self.notebook.add(self.tab_summary, text="  📈 Summary  ")

        self._init_table_tab()
        self._init_chart_tab()
        self._init_summary_tab()

    def _init_table_tab(self):
        self.table_scroll_frame = tk.Frame(self.tab_table, bg=BG_DARK)
        self.table_scroll_frame.pack(fill="both", expand=True)
        tk.Label(self.table_scroll_frame,
                 text="Configure inputs and press  ▶ RUN SIMULATION  to begin.",
                 font=FONT_BODY, bg=BG_DARK, fg=TEXT_DIM).pack(expand=True)

    def _init_chart_tab(self):
        self.chart_frame = tk.Frame(self.tab_chart, bg=BG_DARK)
        self.chart_frame.pack(fill="both", expand=True)
        tk.Label(self.chart_frame, text="Chart will appear after simulation.",
                 font=FONT_BODY, bg=BG_DARK, fg=TEXT_DIM).pack(expand=True)

    def _init_summary_tab(self):
        self.summary_frame = tk.Frame(self.tab_summary, bg=BG_DARK)
        self.summary_frame.pack(fill="both", expand=True)
        tk.Label(self.summary_frame, text="Summary will appear after simulation.",
                 font=FONT_BODY, bg=BG_DARK, fg=TEXT_DIM).pack(expand=True)

    
    def run_simulation(self):
        raw = self.ref_var.get().strip()
        try:
            pages = list(map(int, raw.split()))
            if not pages:
                raise ValueError
        except ValueError:
            messagebox.showerror("Input Error", "Please enter valid space-separated integers for the reference string.")
            return

        frames = self.frame_var.get()
        algo = self.algo_var.get()

        results = {}
        if algo in ("All", "FIFO"):
            results["FIFO"] = fifo(pages, frames)
        if algo in ("All", "LRU"):
            results["LRU"] = lru(pages, frames)
        if algo in ("All", "Optimal"):
            results["Optimal"] = optimal(pages, frames)

        self._render_table(pages, frames, results)
        self._render_chart(results)
        self._render_summary(pages, frames, results)
        self.notebook.select(0)

    def _render_table(self, pages, frames, results):
        for w in self.table_scroll_frame.winfo_children():
            w.destroy()

        canvas = tk.Canvas(self.table_scroll_frame, bg=BG_DARK, highlightthickness=0)
        scrollbar_y = ttk.Scrollbar(self.table_scroll_frame, orient="vertical", command=canvas.yview)
        scrollbar_x = ttk.Scrollbar(self.table_scroll_frame, orient="horizontal", command=canvas.xview)
        inner = tk.Frame(canvas, bg=BG_DARK)

        inner.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
        canvas.create_window((0, 0), window=inner, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar_y.set, xscrollcommand=scrollbar_x.set)

        scrollbar_y.pack(side="right", fill="y")
        scrollbar_x.pack(side="bottom", fill="x")
        canvas.pack(side="left", fill="both", expand=True)

        n = len(pages)
        cell_w = 46
        cell_h = 32

        for algo_idx, (algo_name, result) in enumerate(results.items()):
            frame_states = result["frame_states"]
            faults       = result["faults"]

            
            algo_color = {"FIFO": ACCENT, "LRU": ACCENT2, "Optimal": ACCENT3}[algo_name]
            tk.Label(inner, text=f" {algo_name} ", font=("Segoe UI", 11, "bold"),
                     bg=algo_color, fg="white", padx=8, pady=4).grid(
                row=algo_idx * (frames + 4), column=0, sticky="w", padx=10, pady=(14, 2), columnspan=3)

        
            tk.Label(inner, text="Ref →", font=FONT_SMALL, bg=BG_DARK,
                     fg=TEXT_DIM, width=7).grid(row=algo_idx * (frames + 4) + 1, column=0, padx=(10, 2))
            for j, pg in enumerate(pages):
                is_fault = faults[j]
                bg = FAULT_COLOR if is_fault else HIT_COLOR
                tk.Label(inner, text=str(pg), font=("Courier New", 10, "bold"),
                         bg=bg, fg="white", width=3, relief="flat",
                         height=1).grid(row=algo_idx * (frames + 4) + 1, column=j + 1, padx=1, pady=1)

            
            for f in range(frames):
                tk.Label(inner, text=f"F{f+1}", font=FONT_SMALL, bg=BG_DARK,
                         fg=TEXT_DIM, width=7).grid(row=algo_idx * (frames + 4) + 2 + f, column=0, padx=(10, 2))
                for j in range(n):
                    state = frame_states[j]
                    val = state[f] if f < len(state) else None
                    is_fault = faults[j]
                    if val is None:
                        bg, txt = EMPTY_COLOR, ""
                    else:
                        bg = FAULT_COLOR if is_fault else HIT_COLOR
                        txt = str(val)
                    tk.Label(inner, text=txt, font=FONT_MONO,
                             bg=bg, fg="white", width=3, height=1,
                             relief="flat").grid(row=algo_idx * (frames + 4) + 2 + f,
                                                  column=j + 1, padx=1, pady=1)

            
            total_faults = sum(faults)
            total_hits   = n - total_faults
            tk.Label(inner,
                     text=f"Faults: {total_faults}   Hits: {total_hits}   Hit Rate: {total_hits/n*100:.1f}%",
                     font=FONT_SMALL, bg=BG_DARK, fg=algo_color).grid(
                row=algo_idx * (frames + 4) + 2 + frames,
                column=0, columnspan=n + 2, sticky="w", padx=10, pady=(2, 8))

    def _render_chart(self, results):
        for w in self.chart_frame.winfo_children():
            w.destroy()

        fig = Figure(figsize=(9, 5), facecolor=BG_DARK)
        ax1 = fig.add_subplot(121)
        ax2 = fig.add_subplot(122)

        names   = list(results.keys())
        faults  = [sum(r["faults"]) for r in results.values()]
        n       = len(next(iter(results.values()))["faults"])
        hits    = [n - f for f in faults]
        rates   = [h / n * 100 for h in hits]
        colors  = {"FIFO": ACCENT, "LRU": ACCENT2, "Optimal": ACCENT3}
        bar_colors = [colors[nm] for nm in names]

        
        bars = ax1.bar(names, faults, color=bar_colors, width=0.5, edgecolor="none")
        ax1.set_facecolor(BG_PANEL)
        ax1.set_title("Page Faults", color=TEXT_LIGHT, fontsize=12, fontweight="bold")
        ax1.set_ylabel("Count", color=TEXT_DIM)
        ax1.tick_params(colors=TEXT_DIM)
        ax1.spines[:].set_color(BG_CARD)
        for bar, val in zip(bars, faults):
            ax1.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + 0.2,
                     str(val), ha="center", color=TEXT_LIGHT, fontsize=11, fontweight="bold")

        
        bars2 = ax2.bar(names, rates, color=bar_colors, width=0.5, edgecolor="none")
        ax2.set_facecolor(BG_PANEL)
        ax2.set_title("Hit Rate (%)", color=TEXT_LIGHT, fontsize=12, fontweight="bold")
        ax2.set_ylabel("Hit Rate %", color=TEXT_DIM)
        ax2.set_ylim(0, 100)
        ax2.tick_params(colors=TEXT_DIM)
        ax2.spines[:].set_color(BG_CARD)
        for bar, val in zip(bars2, rates):
            ax2.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + 1,
                     f"{val:.1f}%", ha="center", color=TEXT_LIGHT, fontsize=11, fontweight="bold")

        fig.tight_layout(pad=2.5)
        chart = FigureCanvasTkAgg(fig, master=self.chart_frame)
        chart.draw()
        chart.get_tk_widget().pack(fill="both", expand=True)

    def _render_summary(self, pages, frames, results):
        for w in self.summary_frame.winfo_children():
            w.destroy()

        n = len(pages)
        tk.Label(self.summary_frame, text="Simulation Summary",
                 font=("Segoe UI", 14, "bold"), bg=BG_DARK, fg=TEXT_LIGHT).pack(pady=(20, 4))
        tk.Label(self.summary_frame,
                 text=f"Reference String: {' → '.join(map(str, pages))}   |   Frames: {frames}   |   Total References: {n}",
                 font=FONT_SMALL, bg=BG_DARK, fg=TEXT_DIM).pack()

        card_row = tk.Frame(self.summary_frame, bg=BG_DARK)
        card_row.pack(pady=20, fill="x", padx=30)

        best_algo = min(results, key=lambda k: sum(results[k]["faults"]))
        colors = {"FIFO": ACCENT, "LRU": ACCENT2, "Optimal": ACCENT3}

        for algo_name, result in results.items():
            total_faults = sum(result["faults"])
            total_hits   = n - total_faults
            hit_rate     = total_hits / n * 100
            is_best      = (algo_name == best_algo and len(results) > 1)
            c = colors[algo_name]

            card = tk.Frame(card_row, bg=BG_CARD, padx=20, pady=16, relief="flat")
            card.pack(side="left", fill="both", expand=True, padx=8)

            tk.Label(card, text=algo_name, font=("Segoe UI", 13, "bold"),
                     bg=BG_CARD, fg=c).pack()
            if is_best:
                tk.Label(card, text="✅ Best", font=FONT_SMALL, bg=BG_CARD, fg=ACCENT3).pack()
            tk.Frame(card, bg=c, height=2).pack(fill="x", pady=6)

            for label, val in [("Page Faults", total_faults), ("Page Hits", total_hits), ("Hit Rate", f"{hit_rate:.1f}%"), ("Miss Rate", f"{100-hit_rate:.1f}%")]:
                row = tk.Frame(card, bg=BG_CARD)
                row.pack(fill="x", pady=2)
                tk.Label(row, text=label + ":", font=FONT_SMALL, bg=BG_CARD, fg=TEXT_DIM, width=12, anchor="w").pack(side="left")
                tk.Label(row, text=str(val), font=("Segoe UI", 10, "bold"), bg=BG_CARD, fg=TEXT_LIGHT).pack(side="left")

        
        if len(results) > 1:
            obs = f"🔍 Observation: {best_algo} performs best with fewest page faults ({sum(results[best_algo]['faults'])}) for this reference string."
            tk.Label(self.summary_frame, text=obs, font=FONT_BODY,
                     bg=BG_DARK, fg=ACCENT3, wraplength=700).pack(pady=14)

    def reset(self):
        self.ref_var.set("7 0 1 2 0 3 0 4 2 3 0 3 2 1 2 0 1 7 0 1")
        self.frame_var.set(3)
        self.algo_var.set("All")
        self._init_table_tab()
        self._init_chart_tab()
        self._init_summary_tab()


if __name__ == "__main__":
    app = PageReplacementSimulator()
    app.mainloop()
