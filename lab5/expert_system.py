"""PC Diagnostic Expert System — GUI application using tkinter."""
import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext

from knowledge_base import (
    DiagnosticSystem,
    SYMPTOM_CATEGORIES,
    SECONDARY_SYMPTOMS,
)


class ExpertSystemGUI:
    """Tkinter GUI for the PC diagnostic expert system."""

    def __init__(self, root):
        self.root = root
        self.root.title("PC Diagnostic Expert System")
        self.root.geometry("750x620")
        self.root.resizable(False, False)

        self.engine = DiagnosticSystem()
        self.selected_primary = tk.StringVar()
        self.selected_secondary = tk.StringVar()

        self._build_ui()

    def _build_ui(self):
        # Title
        title_frame = tk.Frame(self.root, bg="#2c3e50", height=50)
        title_frame.pack(fill=tk.X)
        tk.Label(
            title_frame,
            text="PC Diagnostic Expert System",
            font=("Arial", 16, "bold"),
            fg="white",
            bg="#2c3e50",
            pady=10,
        ).pack()

        # Main content
        content = tk.Frame(self.root, padx=20, pady=10)
        content.pack(fill=tk.BOTH, expand=True)

        # Step 1: primary symptom
        tk.Label(
            content,
            text="Step 1: Select the main problem:",
            font=("Arial", 11, "bold"),
            anchor="w",
        ).pack(fill=tk.X, pady=(5, 3))

        self.primary_combo = ttk.Combobox(
            content,
            textvariable=self.selected_primary,
            state="readonly",
            font=("Arial", 10),
            width=60,
        )
        self.primary_combo["values"] = [
            f"{SYMPTOM_CATEGORIES[k]}" for k in SYMPTOM_CATEGORIES
        ]
        self.primary_combo.pack(fill=tk.X, pady=(0, 10))
        self.primary_combo.bind("<<ComboboxSelected>>", self._on_primary_selected)

        # Step 2: secondary symptom
        tk.Label(
            content,
            text="Step 2: Specify the additional detail:",
            font=("Arial", 11, "bold"),
            anchor="w",
        ).pack(fill=tk.X, pady=(5, 3))

        self.secondary_combo = ttk.Combobox(
            content,
            textvariable=self.selected_secondary,
            state="disabled",
            font=("Arial", 10),
            width=60,
        )
        self.secondary_combo.pack(fill=tk.X, pady=(0, 10))

        # Buttons
        btn_frame = tk.Frame(content)
        btn_frame.pack(fill=tk.X, pady=5)

        self.diagnose_btn = tk.Button(
            btn_frame,
            text="Diagnose",
            command=self._run_diagnosis,
            font=("Arial", 11, "bold"),
            bg="#27ae60",
            fg="white",
            padx=20,
            pady=5,
        )
        self.diagnose_btn.pack(side=tk.LEFT, padx=(0, 10))

        self.clear_btn = tk.Button(
            btn_frame,
            text="Clear",
            command=self._clear,
            font=("Arial", 11),
            padx=20,
            pady=5,
        )
        self.clear_btn.pack(side=tk.LEFT, padx=(0, 10))

        self.show_kb_btn = tk.Button(
            btn_frame,
            text="Show Knowledge Base",
            command=self._show_knowledge_base,
            font=("Arial", 11),
            padx=20,
            pady=5,
        )
        self.show_kb_btn.pack(side=tk.LEFT)

        # Results area
        tk.Label(
            content,
            text="Diagnosis Result:",
            font=("Arial", 11, "bold"),
            anchor="w",
        ).pack(fill=tk.X, pady=(15, 3))

        self.result_text = scrolledtext.ScrolledText(
            content, font=("Consolas", 10), height=14, wrap=tk.WORD, state=tk.DISABLED
        )
        self.result_text.pack(fill=tk.BOTH, expand=True)

        # Status bar
        self.status_var = tk.StringVar(value="Select a symptom to begin.")
        tk.Label(
            self.root,
            textvariable=self.status_var,
            bd=1,
            relief=tk.SUNKEN,
            anchor="w",
            padx=5,
            font=("Arial", 9),
        ).pack(fill=tk.X, side=tk.BOTTOM)

    # ---- internal helpers for mapping combo text <-> keys ----

    def _primary_key_from_index(self, index):
        keys = list(SYMPTOM_CATEGORIES.keys())
        return keys[index]

    def _secondary_key_from_index(self, primary_key, index):
        keys = list(SECONDARY_SYMPTOMS[primary_key].keys())
        return keys[index]

    # ---- callbacks ----

    def _on_primary_selected(self, _event=None):
        idx = self.primary_combo.current()
        if idx < 0:
            return
        primary_key = self._primary_key_from_index(idx)
        secondary_options = SECONDARY_SYMPTOMS[primary_key]
        self.secondary_combo.config(state="readonly")
        self.secondary_combo["values"] = list(secondary_options.values())
        self.secondary_combo.set("")
        self.status_var.set("Now select an additional detail.")

    def _run_diagnosis(self):
        p_idx = self.primary_combo.current()
        s_idx = self.secondary_combo.current()

        if p_idx < 0:
            messagebox.showwarning("Warning", "Please select the main problem first.")
            return
        if s_idx < 0:
            messagebox.showwarning("Warning", "Please select an additional detail.")
            return

        primary_key = self._primary_key_from_index(p_idx)
        secondary_key = self._secondary_key_from_index(primary_key, s_idx)

        result = self.engine.diagnose(primary_key, secondary_key)

        self.result_text.config(state=tk.NORMAL)
        self.result_text.delete("1.0", tk.END)

        if result.empty:
            self.result_text.insert(tk.END, "No matching diagnosis found.\n")
            self.status_var.set("No match. Try different symptoms.")
        else:
            row = result.iloc[0]
            output = (
                f"DIAGNOSIS: {row['diagnosis']}\n"
                f"{'-' * 50}\n\n"
                f"Primary symptom : {SYMPTOM_CATEGORIES[primary_key]}\n"
                f"Detail          : {SECONDARY_SYMPTOMS[primary_key][secondary_key]}\n\n"
                f"RECOMMENDATION:\n{row['recommendation']}\n"
            )
            self.result_text.insert(tk.END, output)
            self.status_var.set(f"Diagnosis complete — Rule #{row['rule_id']}")

        self.result_text.config(state=tk.DISABLED)

    def _clear(self):
        self.primary_combo.set("")
        self.secondary_combo.set("")
        self.secondary_combo.config(state="disabled")
        self.result_text.config(state=tk.NORMAL)
        self.result_text.delete("1.0", tk.END)
        self.result_text.config(state=tk.DISABLED)
        self.status_var.set("Select a symptom to begin.")

    def _show_knowledge_base(self):
        kb_window = tk.Toplevel(self.root)
        kb_window.title("Knowledge Base")
        kb_window.geometry("900x500")

        tree = ttk.Treeview(
            kb_window,
            columns=("id", "symptom1", "symptom2", "diagnosis", "recommendation"),
            show="headings",
            height=20,
        )
        tree.heading("id", text="#")
        tree.heading("symptom1", text="Primary Symptom")
        tree.heading("symptom2", text="Detail")
        tree.heading("diagnosis", text="Diagnosis")
        tree.heading("recommendation", text="Recommendation")

        tree.column("id", width=30, anchor="center")
        tree.column("symptom1", width=140)
        tree.column("symptom2", width=150)
        tree.column("diagnosis", width=180)
        tree.column("recommendation", width=380)

        scrollbar = ttk.Scrollbar(kb_window, orient="vertical", command=tree.yview)
        tree.configure(yscrollcommand=scrollbar.set)

        df = self.engine.get_all_rules()
        for _, row in df.iterrows():
            tree.insert(
                "",
                tk.END,
                values=(
                    row["rule_id"],
                    row["symptom_1"],
                    row["symptom_2"],
                    row["diagnosis"],
                    row["recommendation"],
                ),
            )

        tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)


def main():
    root = tk.Tk()
    ExpertSystemGUI(root)
    root.mainloop()


if __name__ == "__main__":
    main()
