from tkinter import *
import math

# Creo la ventana principal, le asigno un nombre, defino el tamaño de la ventana y además uso el método resizable,
# con los dos parámetros a 0, para evitar que se pueda modificar el ancho o el alto de la ventana
window = Tk()
window.title("Calculadora Científica")
window.geometry("400x500")  # Aumento el tamaño para los botones adicionales
window.resizable(0, 0)
window.configure(bg="#f0f0f0")  # Añado un color de fondo más agradable

# Defino las distintas funciones de la calculadora

# Variable global para la expresión
expression = ""


# Función para actualizar el campo de entrada al presionar botones
def btn_click(item):
    global expression
    expression = expression + str(item)
    input_text.set(expression)


# Función para borrar el campo de entrada
def btn_clear():
    global expression
    expression = ""
    input_text.set("")


# Función para calcular el resultado
def btn_equal():
    global expression
    try:
        # Reemplazar funciones especiales antes de evaluar
        expr = expression.replace("sin(", "math.sin(")
        expr = expr.replace("cos(", "math.cos(")
        expr = expr.replace("tan(", "math.tan(")
        expr = expr.replace("log(", "math.log10(")
        expr = expr.replace("ln(", "math.log(")
        expr = expr.replace("sqrt(", "math.sqrt(")
        expr = expr.replace("π", "math.pi")
        expr = expr.replace("e", "math.e")
        expr = expr.replace("^", "**")

        result = str(eval(expr))
        input_text.set(result)
        expression = result
    except:
        input_text.set("Error")
        expression = ""


# Funciones científicas
def scientific_func(func):
    global expression

    if func == "sin":
        expression = "sin(" + expression + ")"
    elif func == "cos":
        expression = "cos(" + expression + ")"
    elif func == "tan":
        expression = "tan(" + expression + ")"
    elif func == "log":
        expression = "log(" + expression + ")"
    elif func == "ln":
        expression = "ln(" + expression + ")"
    elif func == "sqrt":
        expression = "sqrt(" + expression + ")"
    elif func == "fact":
        try:
            n = int(eval(expression))
            expression = str(math.factorial(n))
        except:
            expression = "Error"
    elif func == "pi":
        expression += "π"
    elif func == "e":
        expression += "e"
    elif func == "pow":
        expression += "^"
    elif func == "inv":
        try:
            num = eval(expression)
            expression = str(1 / num)
        except:
            expression = "Error"

    input_text.set(expression)


# Configuración del campo de entrada
input_text = StringVar()

# Marco para el campo de entrada
input_frame = Frame(window, width=400, height=60, bd=0, highlightbackground="black", highlightcolor="black", highlightthickness=1, bg="#f0f0f0")
input_frame.pack(side=TOP, pady=10)

# Campo de entrada
input_field = Entry(input_frame, font=('arial', 18, 'bold'), textvariable=input_text, width=50, bg="#eee", bd=0, justify=RIGHT)
input_field.grid(row=0, column=0)
input_field.pack(ipady=10)

# Marco para los botones
btns_frame = Frame(window, width=400, height=440, bg="#f0f0f0")
btns_frame.pack(pady=5)

# Estilo para los botones
button_params = {
    'height': 2,
    'bd': 0,
    'fg': 'black',
    'cursor': 'hand2',
}

# Colores para diferentes tipos de botones
num_color = "#ffffff"
op_color = "#e6e6e6"
func_color = "#d9d9d9"
eq_color = "#f5c542"
clear_color = "#ff9999"

# Primera fila - Botones científicos
sin = Button(btns_frame, text="sin", width=6, bg=func_color, command=lambda: scientific_func("sin"),  **button_params).grid(row=0, column=0, padx=1, pady=1)
cos = Button(btns_frame, text="cos", width=6, bg=func_color, command=lambda: scientific_func("cos"), **button_params).grid(row=0, column=1, padx=1, pady=1)
tan = Button(btns_frame, text="tan", width=6, bg=func_color, command=lambda: scientific_func("tan"), **button_params).grid(row=0, column=2, padx=1, pady=1)
log = Button(btns_frame, text="log", width=6, bg=func_color, command=lambda: scientific_func("log"), **button_params).grid(row=0, column=3, padx=1, pady=1)
ln = Button(btns_frame, text="ln", width=6, bg=func_color, command=lambda: scientific_func("ln"), **button_params).grid(row=0, column=4, padx=1, pady=1)

# Segunda fila - Más botones científicos
sqrt = Button(btns_frame, text="√", width=6, bg=func_color, command=lambda: scientific_func("sqrt"), **button_params).grid(row=1, column=0, padx=1, pady=1)
fact = Button(btns_frame, text="x!", width=6, bg=func_color, command=lambda: scientific_func("fact"), **button_params).grid(row=1, column=1, padx=1, pady=1)
pi = Button(btns_frame, text="π", width=6, bg=func_color, command=lambda: scientific_func("pi"), **button_params).grid(row=1, column=2, padx=1, pady=1)
e_const = Button(btns_frame, text="e", width=6, bg=func_color, command=lambda: scientific_func("e"), **button_params).grid(row=1, column=3, padx=1, pady=1)
pow_btn = Button(btns_frame, text="x^y", width=6, bg=func_color, command=lambda: scientific_func("pow"),**button_params).grid(row=1, column=4, padx=1, pady=1)

# Tercera fila - Números 7, 8, 9 y operadores
parenth_left = Button(btns_frame, text="(", width=6, bg=op_color, command=lambda: btn_click("("), **button_params).grid( row=2, column=0, padx=1, pady=1)
parenth_right = Button(btns_frame, text=")", width=6, bg=op_color, command=lambda: btn_click(")"), **button_params).grid(row=2, column=1, padx=1, pady=1)
clear = Button(btns_frame, text="C", width=6, bg=clear_color, command=lambda: btn_clear(), **button_params).grid(row=2,  column=2, padx=1, pady=1)
inv = Button(btns_frame, text="1/x", width=6, bg=func_color, command=lambda: scientific_func("inv"), **button_params).grid(row=2, column=3, padx=1, pady=1)
divide = Button(btns_frame, text="/", width=6, bg=op_color, command=lambda: btn_click("/"), **button_params).grid(row=2, column=4, padx=1, pady=1)

# Cuarta fila
seven = Button(btns_frame, text="7", width=6, bg=num_color, command=lambda: btn_click(7), **button_params).grid(row=3, column=0, padx=1,pady=1)
eight = Button(btns_frame, text="8", width=6, bg=num_color, command=lambda: btn_click(8), **button_params).grid(row=3,  column=1, padx=1,  pady=1)
nine = Button(btns_frame, text="9", width=6, bg=num_color, command=lambda: btn_click(9), **button_params).grid(row=3, column=2, padx=1,pady=1)
backspace = Button(btns_frame, text="⌫", width=6, bg=op_color, command=lambda: input_text.set(expression[:-1]), **button_params).grid(row=3, column=3, padx=1, pady=1)
multiply = Button(btns_frame, text="*", width=6, bg=op_color, command=lambda: btn_click("*"), **button_params).grid( row=3, column=4, padx=1, pady=1)

# Quinta fila
four = Button(btns_frame, text="4", width=6, bg=num_color, command=lambda: btn_click(4), **button_params).grid(row=4, column=0, padx=1, pady=1)
five = Button(btns_frame, text="5", width=6, bg=num_color, command=lambda: btn_click(5), **button_params).grid(row=4,column=1, padx=1, pady=1)
six = Button(btns_frame, text="6", width=6, bg=num_color, command=lambda: btn_click(6), **button_params).grid(row=4,column=2,padx=1, pady=1)
mod = Button(btns_frame, text="%", width=6, bg=op_color, command=lambda: btn_click("%"), **button_params).grid(row=4,column=3, padx=1, pady=1)
minus = Button(btns_frame, text="-", width=6, bg=op_color, command=lambda: btn_click("-"), **button_params).grid(row=4, column=4, padx=1, pady=1)

# Sexta fila
one = Button(btns_frame, text="1", width=6, bg=num_color, command=lambda: btn_click(1), **button_params).grid(row=5, column=0, padx=1, pady=1)
two = Button(btns_frame, text="2", width=6, bg=num_color, command=lambda: btn_click(2), **button_params).grid(row=5, column=1,padx=1, pady=1)
three = Button(btns_frame, text="3", width=6, bg=num_color, command=lambda: btn_click(3), **button_params).grid(row=5, column=2, padx=1, pady=1)
plus = Button(btns_frame, text="+", width=6, bg=op_color, command=lambda: btn_click("+"), **button_params).grid(row=5, column=3, padx=1, pady=1)
equals = Button(btns_frame, text="=", width=6, bg=eq_color, command=lambda: btn_equal(), **button_params).grid(row=5, column=4,  padx=1, pady=1)

# Séptima fila
zero = Button(btns_frame, text="0", width=13, bg=num_color, command=lambda: btn_click(0), **button_params).grid(row=6,column=0, columnspan=2, padx=1,pady=1)
point = Button(btns_frame, text=".", width=6, bg=num_color, command=lambda: btn_click("."), **button_params).grid(row=6, column=2, padx=1,pady=1)
exp = Button(btns_frame, text="EXP", width=6, bg=func_color, command=lambda: btn_click("*10**"), **button_params).grid(row=6, column=3, padx=1, pady=1)
ans = Button(btns_frame, text="ANS", width=6, bg=func_color, command=lambda: btn_click(expression), **button_params).grid(row=6, column=4, padx=1, pady=1)

window.mainloop()