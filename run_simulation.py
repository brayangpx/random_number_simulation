# run_simulation.py
import tkinter as tk
from src.ui.linear_gui import LinearGeneratorGUI
from src.ui.additive_gui import AdditiveGeneratorGUI
from src.ui.nonlinear_gui import NonLinearMethodGUI
from src.ui.multiplicative_gui import MultiplicativeGeneratorGUI

def show_linear_generator():
    # Crear la ventana para el generador lineal
    linear_window = tk.Toplevel()
    LinearGeneratorGUI(linear_window)
    linear_window.mainloop()

def show_nonlinear_generator():
#     # Crear la ventana para el generador no lineal
    nonlinear_window = tk.Toplevel()
    NonLinearMethodGUI(nonlinear_window)
    nonlinear_window.mainloop()

def show_multiplicative_generator():
     # Crear la ventana para el generador multiplicativo
     multiplicative_window = tk.Toplevel()
     MultiplicativeGeneratorGUI(multiplicative_window)
     multiplicative_window.mainloop()

def show_additive_generator():
     additive_window = tk.Toplevel()
     AdditiveGeneratorGUI(additive_window)
     additive_window.mainloop()

def main():
    # Ventana principal de la aplicación
    root = tk.Tk()
    root.title("Simulador de Generadores de Números Aleatorios")
    root.geometry("400x300")

    # Etiqueta de bienvenida
    label = tk.Label(root, text="Seleccione el Método de Generación", font=("Helvetica", 14))
    label.pack(pady=20)

    # Botones para cada generador
    btn_linear = tk.Button(root, text="Generador Congruencial Lineal", command=show_linear_generator, width=30)
    btn_linear.pack(pady=10)

    btn_nonlinear = tk.Button(root, text="Generador No Lineal", command=show_nonlinear_generator,  width=30)
    btn_nonlinear.pack(pady=10)

    btn_multiplicative = tk.Button(root, text="Generador Multiplicativo", command=show_multiplicative_generator,  width=30)
    btn_multiplicative.pack(pady=10)

    btn_additive = tk.Button(root, text="Generador Aditivo",command=show_additive_generator, width=30)
    btn_additive.pack(pady=10)

    # Iniciar el loop principal de la aplicación
    root.mainloop()

if __name__ == "__main__":
    main()
