# Bibliotecas para manejar diferentes formatos de archivo
import tkinter as tk
from tkinter import scrolledtext, filedialog, messagebox
import difflib
import os
import csv
import io


#Estructura que trata de importar las bibliotecas opcionales
try:
    import docx
    from PyPDF2 import PdfReader
    from pdfminer.high_level import extract_text as pdf_extract_text

    ALL_FORMATS_AVAILABLE = True
except ImportError:
    ALL_FORMATS_AVAILABLE = False

#Clase principal que encapsula todo el funcionamiento de la aplicación
class TextComparatorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Comparador de Textos")
        self.root.geometry("1000x800")
        self.root.config(bg="#f0f0f0")

        # Configurar el grid principal
        self.root.grid_columnconfigure(0, weight=1)
        self.root.grid_columnconfigure(1, weight=1)
        self.root.grid_rowconfigure(1, weight=1)
        self.root.grid_rowconfigure(5, weight=2)

        # Etiquetas para los cuadros de texto
        tk.Label(root, text="Texto 1", font=("Arial", 12, "bold"), bg="#f0f0f0").grid(row=0, column=0, sticky="w",
                                                                                      padx=10, pady=5)
        tk.Label(root, text="Texto 2", font=("Arial", 12, "bold"), bg="#f0f0f0").grid(row=0, column=1, sticky="w",
                                                                                      padx=10, pady=5)

        # Cuadros de texto para entrada
        self.text1 = scrolledtext.ScrolledText(root, wrap=tk.WORD, width=40, height=10, font=("Consolas", 11))
        self.text1.grid(row=1, column=0, padx=10, pady=5, sticky="nsew")

        self.text2 = scrolledtext.ScrolledText(root, wrap=tk.WORD, width=40, height=10, font=("Consolas", 11))
        self.text2.grid(row=1, column=1, padx=10, pady=5, sticky="nsew")

        # Frames para botones de carga de archivos
        self.btn_frame1 = tk.Frame(root, bg="#f0f0f0")
        self.btn_frame1.grid(row=2, column=0, padx=10, pady=5, sticky="w")

        self.btn_frame2 = tk.Frame(root, bg="#f0f0f0")
        self.btn_frame2.grid(row=2, column=1, padx=10, pady=5, sticky="w")

        # Botones para cargar archivos
        self.load_btn1 = tk.Button(self.btn_frame1, text="Insertar archivo",
                                   command=lambda: self.load_file(self.text1),
                                   bg="#3498db", fg="white", font=("Arial", 10))
        self.load_btn1.pack(side=tk.LEFT, padx=5)

        self.load_btn2 = tk.Button(self.btn_frame2, text="Insertar archivo",
                                   command=lambda: self.load_file(self.text2),
                                   bg="#3498db", fg="white", font=("Arial", 10))
        self.load_btn2.pack(side=tk.LEFT, padx=5)

        # Botón para comparar
        self.compare_button = tk.Button(root, text="Comparar Textos", command=self.compare_texts,
                                        bg="#4CAF50", fg="white", font=("Arial", 12),
                                        relief=tk.RAISED, padx=20, pady=10)
        self.compare_button.grid(row=3, column=0, columnspan=2, pady=10)

        # Etiqueta para el cuadro de resultados
        tk.Label(root, text="Diferencias", font=("Arial", 12, "bold"), bg="#f0f0f0").grid(row=4, column=0, sticky="w",
                                                                                          padx=10, pady=5)

        # Cuadro de texto para mostrar resultados
        self.results_text = scrolledtext.ScrolledText(root, wrap=tk.WORD, width=80, height=20, font=("Consolas", 11))
        self.results_text.grid(row=5, column=0, columnspan=2, padx=10, pady=5, sticky="nsew")
        self.results_text.config(state=tk.DISABLED)  # Inicialmente no editable

        # Configurar etiquetas para formatear el texto de resultados
        self.results_text.tag_configure("title", font=("Arial", 12, "bold"))
        self.results_text.tag_configure("deleted", foreground="red")
        self.results_text.tag_configure("added", foreground="green")
        self.results_text.tag_configure("info", foreground="blue")
        self.results_text.tag_configure("equal", foreground="black")
        self.results_text.tag_configure("summary", foreground="purple")

        # Poner textos de ejemplo
        self.load_examples()

    def load_examples(self):
        """Carga textos de ejemplo en los cuadros de texto"""
        ejemplo1 = """El sol brillaba intensamente sobre las montañas, iluminando el valle con su luz dorada. 
Los pájaros cantaban entre los árboles mientras el río fluía tranquilamente. 
Era un día perfecto de primavera, con un cielo despejado y flores coloridas."""

        ejemplo2 = """El sol brillaba suavemente sobre las colinas, iluminando el valle con su luz dorada. 
Los pájaros cantaban entre los árboles mientras el río fluía serenamente. 
Era un día perfecto de verano, con un cielo despejado y flores coloridas."""

        self.text1.delete(1.0, tk.END)
        self.text1.insert(tk.END, ejemplo1)

        self.text2.delete(1.0, tk.END)
        self.text2.insert(tk.END, ejemplo2)

#Defino el método para la carga de archivos. Hace una verificación de si están disponibles todas las bibliotecas necesarias para leer los distintos tipos de archivos
    def load_file(self, text_widget):
        """Carga un archivo en el widget de texto especificado"""
        # Verificar si están disponibles todas las bibliotecas necesarias
        if not ALL_FORMATS_AVAILABLE:
            messagebox.showwarning(
                "Bibliotecas faltantes",
                "Para abrir todos los formatos de archivo, instala las bibliotecas necesarias:\n"
                "pip install python-docx PyPDF2 pdfminer.six"
            )

        # Definir tipos de archivo para el diálogo
        filetypes = [
            ("Todos los archivos compatibles", "*.txt;*.csv;*.doc;*.docx;*.pdf"),
            ("Archivos de texto", "*.txt"),
            ("Archivos CSV", "*.csv"),
            ("Documentos Word", "*.doc;*.docx"),
            ("Documentos PDF", "*.pdf"),
            ("Todos los archivos", "*.*")
        ]

        # Abrir diálogo para seleccionar archivo
        file_path = filedialog.askopenfilename(filetypes=filetypes)

        if not file_path:
            return  # Usuario canceló la selección

        try:
            # Leer el contenido según la extensión del archivo
            file_content = self.read_file_content(file_path)

            # Insertar el contenido en el widget de texto
            text_widget.delete(1.0, tk.END)
            text_widget.insert(tk.END, file_content)

        except Exception as e:
            messagebox.showerror("Error al cargar archivo", f"No se pudo cargar el archivo:\n{str(e)}")

#Método para leer cada archivo basado en su extensión
    def read_file_content(self, file_path):
        """Lee el contenido de un archivo según su extensión"""
        ext = os.path.splitext(file_path)[1].lower()

        # Archivo de texto plano o CSV
        if ext in ['.txt', '.csv']:
            # Intentar diferentes codificaciones para evitar posibles errores de lectura
            encodings = ['utf-8', 'latin-1', 'cp1252']
            for encoding in encodings:
                try:
                    with open(file_path, 'r', encoding=encoding) as file:
                        if ext == '.csv':
                            # Para CSV, leer y formatear como texto
                            reader = csv.reader(file)
                            lines = []
                            for row in reader:
                                lines.append(' | '.join(row))
                            return '\n'.join(lines)
                        else:
                            # Para TXT, leer directamente
                            return file.read()
                except UnicodeDecodeError:
                    continue

            # Si ninguna codificación funcionó
            raise Exception(f"No se pudo decodificar el archivo {file_path}")

        # Documento Word. Primero verifica si la biblioteca necesaria está disponible. Luego extrae el texto párrafo por párrafo y se une con saltos de línea
        elif ext in ['.doc', '.docx']:
            if not 'docx' in globals():
                raise Exception("Biblioteca python-docx no instalada. Instala con: pip install python-docx")

            doc = docx.Document(file_path)
            full_text = []
            for para in doc.paragraphs:
                full_text.append(para.text)
            return '\n'.join(full_text)

        # Documento PDF. Intenta primero con PyPdf2, que es más rápido, y si falla se intenta con pdfminer.six que es más completo pero más lento
        elif ext == '.pdf':
            if 'PdfReader' not in globals() or 'pdf_extract_text' not in globals():
                raise Exception(
                    "Bibliotecas PyPDF2 o pdfminer.six no instaladas. Instala con: pip install PyPDF2 pdfminer.six")

            # Intentar primero con PyPDF2 (más rápido)
            try:
                reader = PdfReader(file_path)
                text = ""
                for page in reader.pages:
                    text += page.extract_text() + "\n"

                # Si PyPDF2 extrajo texto vacío o muy corto, intentar con pdfminer
                if len(text.strip()) < 50:
                    text = pdf_extract_text(file_path)

                return text
            except Exception as e:
                # Si PyPDF2 falla, intentar con pdfminer
                return pdf_extract_text(file_path)

        else:
            raise Exception(f"Formato de archivo no soportado: {ext}")

#Método para comparar textos. El método se activa al hacer clic en Comparar Textos
    def compare_texts(self):
        """Compara los textos e inserta los resultados en el cuadro de resultados"""
        texto1 = self.text1.get(1.0, tk.END).strip()
        texto2 = self.text2.get(1.0, tk.END).strip()

        if not texto1 or not texto2:
            self.show_results("Por favor, introduce texto en ambos cuadros.")
            return

        # Realizar el análisis
        results = self.analyze_differences(texto1, texto2)

        # Mostrar los resultados
        self.display_results(results)

#Método para analizar las diferencias. Primero se divide el texto en líneas para comparar línea por línea.
#Luego se calcula un ratio de similitud utilizando SequenceMatcher de la biblioteca difflib, este ratio es un porcentaje entre 0 y 100
    def analyze_differences(self, text1, text2):
        """Analiza las diferencias entre los dos textos"""
        # Dividir los textos en líneas
        text1_lines = text1.splitlines()
        text2_lines = text2.splitlines()

        # Calcular la similitud
        sequence_matcher = difflib.SequenceMatcher(None, text1, text2)
        similarity_ratio = sequence_matcher.ratio() * 100

        # Obtener las diferencias en formato ndiff
        ndiff_output = list(difflib.ndiff(text1_lines, text2_lines))

        # Encontrar los bloques de operaciones
        opcodes = sequence_matcher.get_opcodes()
        operations = []

        for tag, i1, i2, j1, j2 in opcodes:
            if tag != 'equal':
                operations.append({
                    'operation': tag,
                    'text1_content': text1[i1:i2],
                    'text2_content': text2[j1:j2]
                })

        # Crear resumen
        summary = []
        for op in operations:
            if op['operation'] == 'replace':
                summary.append(f"Reemplazo: '{op['text1_content']}' → '{op['text2_content']}'")
            elif op['operation'] == 'delete':
                summary.append(f"Eliminado: '{op['text1_content']}'")
            elif op['operation'] == 'insert':
                summary.append(f"Insertado: '{op['text2_content']}'")

        return {
            'similarity_percentage': similarity_ratio,
            'ndiff': ndiff_output,
            'summary': summary
        }
#Este método muestra los resultados del análisis.
    def display_results(self, results):
        """Muestra los resultados formateados en el cuadro de texto de resultados"""
        # Habilitar la edición del cuadro de resultados
        self.results_text.config(state=tk.NORMAL)
        self.results_text.delete(1.0, tk.END)

        # Añadir el porcentaje de similitud
        self.results_text.insert(tk.END, "Porcentaje de Similitud:\n", "title")
        self.results_text.insert(tk.END, f"{results['similarity_percentage']:.2f}%\n\n")

        # Añadir el resumen de diferencias
        self.results_text.insert(tk.END, "Resumen de Diferencias:\n", "title")
        if results['summary']:
            for item in results['summary']:
                self.results_text.insert(tk.END, f"• {item}\n", "summary")
        else:
            self.results_text.insert(tk.END, "No se encontraron diferencias.\n")

        # Añadir las diferencias detalladas
        self.results_text.insert(tk.END, "\nDiferencias Detalladas (formato ndiff):\n", "title")
        for line in results['ndiff']:
            if line.startswith('- '):
                self.results_text.insert(tk.END, line + "\n", "deleted")
            elif line.startswith('+ '):
                self.results_text.insert(tk.END, line + "\n", "added")
            elif line.startswith('? '):
                self.results_text.insert(tk.END, line + "\n", "info")
            else:
                self.results_text.insert(tk.END, line + "\n", "equal")

        # Explicación de los símbolos
        self.results_text.insert(tk.END, "\nGuía de Símbolos:\n", "title")
        self.results_text.insert(tk.END,
                                 "- Línea presente en el texto 1 pero no en el texto 2 (eliminada o modificada)\n",
                                 "deleted")
        self.results_text.insert(tk.END,
                                 "+ Línea presente en el texto 2 pero no en el texto 1 (añadida o modificada)\n",
                                 "added")
        self.results_text.insert(tk.END,
                                 "? Marcador que indica exactamente dónde están las diferencias (^ señala caracteres específicos)\n",
                                 "info")
        self.results_text.insert(tk.END, "  Línea idéntica en ambos textos\n", "equal")

        # Deshabilitar la edición del cuadro de resultados
        self.results_text.config(state=tk.DISABLED)


if __name__ == "__main__":
    root = tk.Tk()
    app = TextComparatorApp(root)
    root.mainloop()