"""
Juntar Planilhas - App Desktop
--------------------------------
Interface gráfica para unificar todas as planilhas (.xlsx) de uma pasta
em um único arquivo Excel.

Requisitos (instalar uma vez):
    pip install pandas openpyxl

Como rodar:
    python juntar_planilhas.py
"""

import os
import threading
import tkinter as tk
from tkinter import ttk, filedialog, messagebox

import pandas as pd


class JuntarPlanilhasApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Juntar Planilhas")
        self.root.geometry("620x480")
        self.root.minsize(560, 420)

        self.pasta_origem = tk.StringVar()
        self.arquivo_destino = tk.StringVar(value="planilha_unificada.xlsx")

        self._montar_interface()

    # ------------------------------------------------------------------
    # Interface
    # ------------------------------------------------------------------
    def _montar_interface(self):
        padding = {"padx": 12, "pady": 6}

        # --- Pasta de origem ---
        frame_origem = ttk.LabelFrame(self.root, text="1. Pasta com as planilhas")
        frame_origem.pack(fill="x", **padding)

        entry_origem = ttk.Entry(frame_origem, textvariable=self.pasta_origem)
        entry_origem.pack(side="left", fill="x", expand=True, padx=(10, 6), pady=10)

        ttk.Button(
            frame_origem, text="Escolher pasta...", command=self.escolher_pasta
        ).pack(side="left", padx=(0, 10), pady=10)

        # --- Arquivo de destino ---
        frame_destino = ttk.LabelFrame(self.root, text="2. Salvar resultado como")
        frame_destino.pack(fill="x", **padding)

        entry_destino = ttk.Entry(frame_destino, textvariable=self.arquivo_destino)
        entry_destino.pack(side="left", fill="x", expand=True, padx=(10, 6), pady=10)

        ttk.Button(
            frame_destino, text="Escolher local...", command=self.escolher_destino
        ).pack(side="left", padx=(0, 10), pady=10)

        # --- Botão de ação ---
        self.botao_juntar = ttk.Button(
            self.root, text="Juntar planilhas", command=self.iniciar_juncao
        )
        self.botao_juntar.pack(pady=(6, 4))

        self.barra_progresso = ttk.Progressbar(self.root, mode="indeterminate")
        self.barra_progresso.pack(fill="x", padx=12, pady=(0, 6))

        # --- Log ---
        frame_log = ttk.LabelFrame(self.root, text="Progresso")
        frame_log.pack(fill="both", expand=True, **padding)

        self.texto_log = tk.Text(frame_log, height=12, state="disabled", wrap="word")
        self.texto_log.pack(side="left", fill="both", expand=True, padx=(10, 0), pady=10)

        scrollbar = ttk.Scrollbar(frame_log, command=self.texto_log.yview)
        scrollbar.pack(side="right", fill="y", padx=(0, 10), pady=10)
        self.texto_log.config(yscrollcommand=scrollbar.set)

    # ------------------------------------------------------------------
    # Ações da interface
    # ------------------------------------------------------------------
    def escolher_pasta(self):
        pasta = filedialog.askdirectory(title="Selecione a pasta com as planilhas")
        if pasta:
            self.pasta_origem.set(pasta)

    def escolher_destino(self):
        caminho = filedialog.asksaveasfilename(
            title="Salvar planilha unificada como",
            defaultextension=".xlsx",
            filetypes=[("Arquivo Excel", "*.xlsx")],
            initialfile="planilha_unificada.xlsx",
        )
        if caminho:
            self.arquivo_destino.set(caminho)

    def log(self, mensagem):
        self.texto_log.config(state="normal")
        self.texto_log.insert("end", mensagem + "\n")
        self.texto_log.see("end")
        self.texto_log.config(state="disabled")

    def limpar_log(self):
        self.texto_log.config(state="normal")
        self.texto_log.delete("1.0", "end")
        self.texto_log.config(state="disabled")

    def iniciar_juncao(self):
        pasta = self.pasta_origem.get().strip()
        destino = self.arquivo_destino.get().strip()

        if not pasta:
            messagebox.showwarning("Atenção", "Escolha a pasta com as planilhas.")
            return
        if not os.path.isdir(pasta):
            messagebox.showerror("Erro", "A pasta escolhida não existe.")
            return
        if not destino:
            messagebox.showwarning("Atenção", "Escolha onde salvar o resultado.")
            return

        # Roda em thread separada para não travar a interface
        self.botao_juntar.config(state="disabled")
        self.barra_progresso.start(10)
        self.limpar_log()

        thread = threading.Thread(
            target=self.executar_juncao, args=(pasta, destino), daemon=True
        )
        thread.start()

    # ------------------------------------------------------------------
    # Lógica de negócio (baseada no script original do usuário)
    # ------------------------------------------------------------------
    def executar_juncao(self, pasta, destino):
        try:
            dfs = []
            arquivos = sorted(f for f in os.listdir(pasta) if f.endswith(".xlsx"))

            if not arquivos:
                self.root.after(
                    0, lambda: self.log("Nenhum arquivo .xlsx encontrado nessa pasta.")
                )
                return

            for arquivo in arquivos:
                caminho = os.path.join(pasta, arquivo)
                xls = pd.ExcelFile(caminho)

                for aba in xls.sheet_names:
                    msg = f"{arquivo} -> {aba}"
                    self.root.after(0, lambda m=msg: self.log(m))
                    df = pd.read_excel(caminho, sheet_name=aba)
                    dfs.append(df)

            resultado = pd.concat(dfs, ignore_index=True)
            resultado.to_excel(destino, index=False)

            total_linhas = len(resultado)
            self.root.after(
                0,
                lambda: self.log(
                    f"\nConcluído! {len(arquivos)} arquivo(s) processado(s), "
                    f"{total_linhas} linha(s) no total.\nSalvo em: {destino}"
                ),
            )
            self.root.after(
                0,
                lambda: messagebox.showinfo(
                    "Sucesso", f"Planilha unificada salva em:\n{destino}"
                ),
            )

        except Exception as e:
            erro = str(e)
            self.root.after(0, lambda: self.log(f"\nErro: {erro}"))
            self.root.after(0, lambda: messagebox.showerror("Erro", erro))

        finally:
            self.root.after(0, self.finalizar_juncao)

    def finalizar_juncao(self):
        self.barra_progresso.stop()
        self.botao_juntar.config(state="normal")


def main():
    root = tk.Tk()
    try:
        style = ttk.Style()
        if "vista" in style.theme_names():
            style.theme_use("vista")
        elif "clam" in style.theme_names():
            style.theme_use("clam")
    except Exception:
        pass

    app = JuntarPlanilhasApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()