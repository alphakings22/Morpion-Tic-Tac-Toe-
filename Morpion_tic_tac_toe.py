import tkinter as tk
from tkinter import messagebox
import json
import os

root = tk.Tk()
root.title("Tic Tac Toe 🎮")
root.configure(bg="#1e1e2f")  # Thème sombre

# Charger les scores depuis un fichier JSON
if os.path.exists("scores.json"):
    with open("scores.json", "r") as f:
        scores = json.load(f)
else:
    scores = {"X": 0, "O": 0}

players = "X"
plateau = [["" for _ in range(3)] for _ in range(3)]
boutons = [[None for _ in range(3)] for _ in range(3)]

label_info = tk.Label(root, text=f"Tour du joueur {players}",
                      font=("Consolas", 18, "bold"),
                      fg="#f5f5f5", bg="#1e1e2f")
label_info.grid(row=3, column=0, columnspan=3, pady=10)

# Label pour afficher les scores
label_scores = tk.Label(root, text=f"Scores - X: {scores['X']} | O: {scores['O']}",
                        font=("Consolas", 14), fg="white", bg="#1e1e2f")
label_scores.grid(row=5, column=0, columnspan=3, pady=5)


def verifier_victoiry():
    for i in range(3):
        if plateau[i][0] == plateau[i][1] == plateau[i][2] != "":
            return [(i, 0), (i, 1), (i, 2)]
    for j in range(3):
        if plateau[0][j] == plateau[1][j] == plateau[2][j] != "":
            return [(0, j), (1, j), (2, j)]
    if plateau[0][0] == plateau[1][1] == plateau[2][2] != "":
        return [(0, 0), (1, 1), (2, 2)]
    if plateau[0][2] == plateau[1][1] == plateau[2][0] != "":
        return [(0, 2), (1, 1), (2, 0)]
    return None


def animation_victoiry(cases, couleur1="#ffeb3b", couleur2="#2e2e3e", step=0):
    for (i, j) in cases:
        boutons[i][j].config(bg=couleur1 if step % 2 == 0 else couleur2)
    if step < 6:
        root.after(300, animation_victoiry, cases, couleur1, couleur2, step + 1)
    else:
        #  Mise à jour du score
        scores[players] += 1
        label_scores.config(text=f"Scores - X: {scores['X']} | O: {scores['O']}")
        # Sauvegarde JSON
        with open("scores.json", "w") as f:
            json.dump(scores, f)
        messagebox.showinfo("Félicitations !", f"{players} a gagné ")
        reset()


def clic(i, j):
    global players
    if plateau[i][j] == "":
        plateau[i][j] = players
        couleur = "#4fc3f7" if players == "X" else "#f06292"
        boutons[i][j].config(text=players, fg=couleur, state="disabled")

        cases_gagnantes = verifier_victoiry()
        if cases_gagnantes:
            animation_victoiry(cases_gagnantes)
        elif all(all(cell != "" for cell in row) for row in plateau):
            messagebox.showinfo("Match nul", "Personne n'a gagné ")
            reset()
        else:
            players = "O" if players == "X" else "X"
            label_info.config(text=f"Tour du joueur {players}")


def reset():
    global players, plateau
    players = "X"
    plateau = [["" for _ in range(3)] for _ in range(3)]
    label_info.config(text=f"Tour du joueur {players}")
    for i in range(3):
        for j in range(3):
            boutons[i][j].config(text="", state="normal", bg="#2e2e3e")


# Création des boutons
for i in range(3):
    for j in range(3):
        bouton = tk.Button(root, text="", font=("Consolas", 28, "bold"),
                           width=5, height=2, bg="#2e2e3e", fg="#f5f5f5",
                           activebackground="#3e3e5e",
                           command=lambda i=i, j=j: clic(i, j))
        bouton.grid(row=i, column=j, padx=5, pady=5)
        boutons[i][j] = bouton

btn_reset = tk.Button(root, text="Rejouer ", font=("Consolas", 14, "bold"),
                      bg="#4caf50", fg="white", activebackground="#66bb6a",
                      command=reset)
btn_reset.grid(row=4, column=0, columnspan=3, pady=10)

root.mainloop()
