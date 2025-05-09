import sys
from PyQt6.QtWidgets import (QApplication, QMainWindow, QLabel, QLineEdit, 
                            QPushButton, QVBoxLayout, QHBoxLayout, QWidget, 
                            QStackedWidget, QTableWidget, QTableWidgetItem,
                            QMessageBox, QHeaderView, QComboBox, QDateEdit)
from PyQt6.QtCore import Qt, QDate
import mysql.connector
from mysql.connector import Error

class COMEXApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Sistema COMEX")
        self.setGeometry(100, 100, 1100, 750)
        self.connect_to_db()
        self.setup_ui()
        
    def connect_to_db(self):
        try:
            self.connection = mysql.connector.connect(
                host='localhost',
                user='root',
                password='mysql',
                database='comex'
            )
            if self.connection.is_connected():
                print("Conexión exitosa a MySQL")
        except Error as e:
            print(f"Error al conectar a MySQL: {e}")
            QMessageBox.critical(self, "Error", f"No se pudo conectar a la base de datos:\n{e}")

    def setup_ui(self):
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QHBoxLayout(central_widget)
        
        menu_layout = QVBoxLayout()
        menu_layout.setAlignment(Qt.AlignmentFlag.AlignTop)

        btn_style = """
            QPushButton {
                padding: 10px;
                font-size: 14px;
                min-width: 120px;
                border: 1px solid #444;
                border-radius: 5px;
                background-color: #2d2d2d;
                color: #ffffff;
            }
            QPushButton:hover {
                background-color: #3c3c3c;
            }
        """

        self.btn_clientes = QPushButton("Clientes")
        self.btn_clientes.setStyleSheet(btn_style)
        self.btn_clientes.clicked.connect(lambda: self.show_section(1))
        
        self.btn_articulos = QPushButton("Artículos")
        self.btn_articulos.setStyleSheet(btn_style)
        self.btn_articulos.clicked.connect(lambda: self.show_section(2))
        
        self.btn_categorias = QPushButton("Categorías")
        self.btn_categorias.setStyleSheet(btn_style)
        self.btn_categorias.clicked.connect(lambda: self.show_section(3))
        
        self.btn_ventas = QPushButton("Ventas")
        self.btn_ventas.setStyleSheet(btn_style)
        self.btn_ventas.clicked.connect(lambda: self.show_section(4))
        
        self.btn_detalle_ventas = QPushButton("Detalle Ventas")
        self.btn_detalle_ventas.setStyleSheet(btn_style)
        self.btn_detalle_ventas.clicked.connect(lambda: self.show_section(5))
        
        menu_layout.addWidget(self.btn_clientes)
        menu_layout.addWidget(self.btn_articulos)
        menu_layout.addWidget(self.btn_categorias)
        menu_layout.addWidget(self.btn_ventas)
        menu_layout.addWidget(self.btn_detalle_ventas)
        menu_layout.addStretch()

        self.stacked_widget = QStackedWidget()
        
        # Crear secciones (nombres de métodos corregidos)
        self.create_clientes_section()
        self.create_articulos_section()
        self.create_categorias_section()
        self.create_ventas_section()
        self.create_detalle_ventas_section()

        main_layout.addLayout(menu_layout, 1)
        main_layout.addWidget(self.stacked_widget, 4)
    
    def show_section(self, index):
        self.stacked_widget.setCurrentIndex(index - 1)
        if index == 1:
            self.load_clientes()
        elif index == 2:
            self.load_articulos()
            self.load_categorias_combo()
        elif index == 3:
            self.load_categorias()
        elif index == 4:
            self.load_ventas()
            self.load_clientes_combo()
        elif index == 5:
            self.load_detalle_ventas()
            self.load_ventas_combo()
            self.load_articulos_combo()

    # Sección de Clientes
    def create_clientes_section(self):
        widget = QWidget()
        layout = QVBoxLayout(widget)

        form_layout = QVBoxLayout()
        form_layout.setSpacing(10)
        
        self.entry_telefono_cliente = self.create_form_field("Teléfono (10 dígitos):", form_layout)
        self.entry_nombre_cliente = self.create_form_field("Nombre completo:", form_layout)
        self.entry_direccion_cliente = self.create_form_field("Dirección:", form_layout)
        self.entry_rfc_cliente = self.create_form_field("RFC (13 caracteres):", form_layout)
        self.entry_correo_cliente = self.create_form_field("Correo electrónico:", form_layout)

        btn_layout = QHBoxLayout()
        btn_layout.setSpacing(10)

        self.btn_guardar_cliente = QPushButton("Guardar")
        self.btn_guardar_cliente.setStyleSheet("background-color: #4CAF50; color: white;")
        self.btn_guardar_cliente.clicked.connect(self.save_cliente)

        self.btn_editar_cliente = QPushButton("Editar")
        self.btn_editar_cliente.setStyleSheet("background-color: #2196F3; color: white;")
        self.btn_editar_cliente.clicked.connect(self.edit_cliente)

        self.btn_eliminar_cliente = QPushButton("Eliminar")
        self.btn_eliminar_cliente.setStyleSheet("background-color: #f44336; color: white;")
        self.btn_eliminar_cliente.clicked.connect(self.delete_cliente)

        self.btn_leer_clientes = QPushButton("Leer")
        self.btn_leer_clientes.setStyleSheet("background-color: #607D8B; color: white;")
        self.btn_leer_clientes.clicked.connect(self.load_clientes)

        btn_layout.addWidget(self.btn_guardar_cliente)
        btn_layout.addWidget(self.btn_editar_cliente)
        btn_layout.addWidget(self.btn_eliminar_cliente)
        btn_layout.addWidget(self.btn_leer_clientes)

        self.table_clientes = QTableWidget()
        self.table_clientes.setColumnCount(5)
        self.table_clientes.setHorizontalHeaderLabels(["Teléfono", "Nombre", "Dirección", "RFC", "Correo"])
        self.table_clientes.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.table_clientes.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        self.table_clientes.cellClicked.connect(self.load_cliente_from_table)

        layout.addLayout(form_layout)
        layout.addLayout(btn_layout)
        layout.addWidget(self.table_clientes)
        self.stacked_widget.addWidget(widget)

    # Sección de Artículos
    def create_articulos_section(self):
        widget = QWidget()
        layout = QVBoxLayout(widget)

        form_layout = QVBoxLayout()
        form_layout.setSpacing(10)
        
        self.entry_codigo_articulo = self.create_form_field("Código (13 caracteres):", form_layout)
        self.entry_nombre_articulo = self.create_form_field("Nombre:", form_layout)
        self.entry_precio_articulo = self.create_form_field("Precio:", form_layout)
        self.entry_costo_articulo = self.create_form_field("Costo:", form_layout)
        self.entry_existencia_articulo = self.create_form_field("Existencia:", form_layout)
        self.entry_unidad_articulo = self.create_form_field("Unidad:", form_layout)
        
        # ComboBox para categoría
        h_layout = QHBoxLayout()
        lbl_categoria = QLabel("Categoría:")
        lbl_categoria.setFixedWidth(150)
        self.combo_categoria_articulo = QComboBox()
        h_layout.addWidget(lbl_categoria)
        h_layout.addWidget(self.combo_categoria_articulo)
        form_layout.addLayout(h_layout)

        btn_layout = QHBoxLayout()
        btn_layout.setSpacing(10)

        self.btn_guardar_articulo = QPushButton("Guardar")
        self.btn_guardar_articulo.setStyleSheet("background-color: #4CAF50; color: white;")
        self.btn_guardar_articulo.clicked.connect(self.save_articulo)

        self.btn_editar_articulo = QPushButton("Editar")
        self.btn_editar_articulo.setStyleSheet("background-color: #2196F3; color: white;")
        self.btn_editar_articulo.clicked.connect(self.edit_articulo)

        self.btn_eliminar_articulo = QPushButton("Eliminar")
        self.btn_eliminar_articulo.setStyleSheet("background-color: #f44336; color: white;")
        self.btn_eliminar_articulo.clicked.connect(self.delete_articulo)

        self.btn_leer_articulos = QPushButton("Leer")
        self.btn_leer_articulos.setStyleSheet("background-color: #607D8B; color: white;")
        self.btn_leer_articulos.clicked.connect(self.load_articulos)

        btn_layout.addWidget(self.btn_guardar_articulo)
        btn_layout.addWidget(self.btn_editar_articulo)
        btn_layout.addWidget(self.btn_eliminar_articulo)
        btn_layout.addWidget(self.btn_leer_articulos)

        self.table_articulos = QTableWidget()
        self.table_articulos.setColumnCount(7)
        self.table_articulos.setHorizontalHeaderLabels(["Código", "Nombre", "Precio", "Costo", "Existencia", "Unidad", "Categoría"])
        self.table_articulos.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.table_articulos.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        self.table_articulos.cellClicked.connect(self.load_articulo_from_table)

        layout.addLayout(form_layout)
        layout.addLayout(btn_layout)
        layout.addWidget(self.table_articulos)
        self.stacked_widget.addWidget(widget)

    # Sección de Categorías
    def create_categorias_section(self):
        widget = QWidget()
        layout = QVBoxLayout(widget)

        form_layout = QVBoxLayout()
        form_layout.setSpacing(10)
        
        self.entry_id_categoria = self.create_form_field("ID Categoría:", form_layout)
        self.entry_nombre_categoria = self.create_form_field("Nombre:", form_layout)

        btn_layout = QHBoxLayout()
        btn_layout.setSpacing(10)

        self.btn_guardar_categoria = QPushButton("Guardar")
        self.btn_guardar_categoria.setStyleSheet("background-color: #4CAF50; color: white;")
        self.btn_guardar_categoria.clicked.connect(self.save_categoria)

        self.btn_editar_categoria = QPushButton("Editar")
        self.btn_editar_categoria.setStyleSheet("background-color: #2196F3; color: white;")
        self.btn_editar_categoria.clicked.connect(self.edit_categoria)

        self.btn_eliminar_categoria = QPushButton("Eliminar")
        self.btn_eliminar_categoria.setStyleSheet("background-color: #f44336; color: white;")
        self.btn_eliminar_categoria.clicked.connect(self.delete_categoria)

        self.btn_leer_categorias = QPushButton("Leer")
        self.btn_leer_categorias.setStyleSheet("background-color: #607D8B; color: white;")
        self.btn_leer_categorias.clicked.connect(self.load_categorias)

        btn_layout.addWidget(self.btn_guardar_categoria)
        btn_layout.addWidget(self.btn_editar_categoria)
        btn_layout.addWidget(self.btn_eliminar_categoria)
        btn_layout.addWidget(self.btn_leer_categorias)

        self.table_categorias = QTableWidget()
        self.table_categorias.setColumnCount(2)
        self.table_categorias.setHorizontalHeaderLabels(["ID Categoría", "Nombre"])
        self.table_categorias.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.table_categorias.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        self.table_categorias.cellClicked.connect(self.load_categoria_from_table)

        layout.addLayout(form_layout)
        layout.addLayout(btn_layout)
        layout.addWidget(self.table_categorias)
        self.stacked_widget.addWidget(widget)

    # Sección de Ventas
    def create_ventas_section(self):
        widget = QWidget()
        layout = QVBoxLayout(widget)

        form_layout = QVBoxLayout()
        form_layout.setSpacing(10)
        
        self.entry_id_venta = self.create_form_field("ID Venta:", form_layout)
        
        # Fecha
        h_layout_fecha = QHBoxLayout()
        lbl_fecha = QLabel("Fecha:")
        lbl_fecha.setFixedWidth(150)
        self.date_venta = QDateEdit(QDate.currentDate())
        self.date_venta.setCalendarPopup(True)
        h_layout_fecha.addWidget(lbl_fecha)
        h_layout_fecha.addWidget(self.date_venta)
        form_layout.addLayout(h_layout_fecha)
        
        self.entry_importe_venta = self.create_form_field("Importe:", form_layout)
        self.entry_iva_venta = self.create_form_field("IVA:", form_layout)
        self.entry_total_venta = self.create_form_field("Total:", form_layout)
        
        # ComboBox para cliente
        h_layout_cliente = QHBoxLayout()
        lbl_cliente = QLabel("Cliente:")
        lbl_cliente.setFixedWidth(150)
        self.combo_cliente_venta = QComboBox()
        h_layout_cliente.addWidget(lbl_cliente)
        h_layout_cliente.addWidget(self.combo_cliente_venta)
        form_layout.addLayout(h_layout_cliente)

        btn_layout = QHBoxLayout()
        btn_layout.setSpacing(10)

        self.btn_guardar_venta = QPushButton("Guardar")
        self.btn_guardar_venta.setStyleSheet("background-color: #4CAF50; color: white;")
        self.btn_guardar_venta.clicked.connect(self.save_venta)

        self.btn_editar_venta = QPushButton("Editar")
        self.btn_editar_venta.setStyleSheet("background-color: #2196F3; color: white;")
        self.btn_editar_venta.clicked.connect(self.edit_venta)

        self.btn_eliminar_venta = QPushButton("Eliminar")
        self.btn_eliminar_venta.setStyleSheet("background-color: #f44336; color: white;")
        self.btn_eliminar_venta.clicked.connect(self.delete_venta)

        self.btn_leer_ventas = QPushButton("Leer")
        self.btn_leer_ventas.setStyleSheet("background-color: #607D8B; color: white;")
        self.btn_leer_ventas.clicked.connect(self.load_ventas)

        btn_layout.addWidget(self.btn_guardar_venta)
        btn_layout.addWidget(self.btn_editar_venta)
        btn_layout.addWidget(self.btn_eliminar_venta)
        btn_layout.addWidget(self.btn_leer_ventas)

        self.table_ventas = QTableWidget()
        self.table_ventas.setColumnCount(6)
        self.table_ventas.setHorizontalHeaderLabels(["ID Venta", "Fecha", "Importe", "IVA", "Total", "Cliente"])
        self.table_ventas.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.table_ventas.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        self.table_ventas.cellClicked.connect(self.load_venta_from_table)

        layout.addLayout(form_layout)
        layout.addLayout(btn_layout)
        layout.addWidget(self.table_ventas)
        self.stacked_widget.addWidget(widget)

    # Sección de Detalle Ventas
    def create_detalle_ventas_section(self):
        widget = QWidget()
        layout = QVBoxLayout(widget)

        form_layout = QVBoxLayout()
        form_layout.setSpacing(10)
        
        # ComboBox para venta
        h_layout_venta = QHBoxLayout()
        lbl_venta = QLabel("Venta:")
        lbl_venta.setFixedWidth(150)
        self.combo_venta_detalle = QComboBox()
        h_layout_venta.addWidget(lbl_venta)
        h_layout_venta.addWidget(self.combo_venta_detalle)
        form_layout.addLayout(h_layout_venta)
        
        # ComboBox para artículo
        h_layout_articulo = QHBoxLayout()
        lbl_articulo = QLabel("Artículo:")
        lbl_articulo.setFixedWidth(150)
        self.combo_articulo_detalle = QComboBox()
        h_layout_articulo.addWidget(lbl_articulo)
        h_layout_articulo.addWidget(self.combo_articulo_detalle)
        form_layout.addLayout(h_layout_articulo)
        
        self.entry_cantidad_detalle = self.create_form_field("Cantidad:", form_layout)
        self.entry_precio_detalle = self.create_form_field("Precio:", form_layout)
        self.entry_importe_detalle = self.create_form_field("Importe:", form_layout)

        btn_layout = QHBoxLayout()
        btn_layout.setSpacing(10)

        self.btn_guardar_detalle = QPushButton("Guardar")
        self.btn_guardar_detalle.setStyleSheet("background-color: #4CAF50; color: white;")
        self.btn_guardar_detalle.clicked.connect(self.save_detalle_venta)

        self.btn_editar_detalle = QPushButton("Editar")
        self.btn_editar_detalle.setStyleSheet("background-color: #2196F3; color: white;")
        self.btn_editar_detalle.clicked.connect(self.edit_detalle_venta)

        self.btn_eliminar_detalle = QPushButton("Eliminar")
        self.btn_eliminar_detalle.setStyleSheet("background-color: #f44336; color: white;")
        self.btn_eliminar_detalle.clicked.connect(self.delete_detalle_venta)

        self.btn_leer_detalles = QPushButton("Leer")
        self.btn_leer_detalles.setStyleSheet("background-color: #607D8B; color: white;")
        self.btn_leer_detalles.clicked.connect(self.load_detalle_ventas)

        btn_layout.addWidget(self.btn_guardar_detalle)
        btn_layout.addWidget(self.btn_editar_detalle)
        btn_layout.addWidget(self.btn_eliminar_detalle)
        btn_layout.addWidget(self.btn_leer_detalles)

        self.table_detalle_ventas = QTableWidget()
        self.table_detalle_ventas.setColumnCount(6)
        self.table_detalle_ventas.setHorizontalHeaderLabels(["ID Venta", "Venta", "Código Artículo", "Artículo", "Cantidad", "Precio", "Importe"])
        self.table_detalle_ventas.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.table_detalle_ventas.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        self.table_detalle_ventas.cellClicked.connect(self.load_detalle_from_table)

        layout.addLayout(form_layout)
        layout.addLayout(btn_layout)
        layout.addWidget(self.table_detalle_ventas)
        self.stacked_widget.addWidget(widget)

    def create_form_field(self, label_text, layout):
        h_layout = QHBoxLayout()
        lbl = QLabel(label_text)
        lbl.setFixedWidth(150)
        entry = QLineEdit()
        h_layout.addWidget(lbl)
        h_layout.addWidget(entry)
        layout.addLayout(h_layout)
        return entry

    # Métodos para Clientes
    def load_clientes(self):
        try:
            cursor = self.connection.cursor()
            cursor.execute("SELECT telefono, nombre, direccion, rfc, correo FROM Clientes")
            clientes = cursor.fetchall()
            self.table_clientes.setRowCount(len(clientes))
            for row_idx, row_data in enumerate(clientes):
                for col_idx, col_data in enumerate(row_data):
                    self.table_clientes.setItem(row_idx, col_idx, QTableWidgetItem(str(col_data)))
        except Error as e:
            QMessageBox.critical(self, "Error", f"Error al cargar clientes:\n{e}")

    def save_cliente(self):
        telefono = self.entry_telefono_cliente.text().strip()
        nombre = self.entry_nombre_cliente.text().strip()
        direccion = self.entry_direccion_cliente.text().strip()
        rfc = self.entry_rfc_cliente.text().strip()
        correo = self.entry_correo_cliente.text().strip()

        if not telefono or not nombre:
            QMessageBox.warning(self, "Advertencia", "Teléfono y Nombre son campos obligatorios")
            return

        if len(telefono) != 10 or not telefono.isdigit():
            QMessageBox.warning(self, "Advertencia", "El teléfono debe tener 10 dígitos")
            return

        try:
            cursor = self.connection.cursor()
            cursor.execute(
                "INSERT INTO Clientes (telefono, nombre, direccion, rfc, correo) VALUES (%s, %s, %s, %s, %s)",
                (telefono, nombre, direccion, rfc, correo)
            )
            self.connection.commit()
            QMessageBox.information(self, "Éxito", "Cliente guardado correctamente")
            self.load_clientes()
            self.clear_cliente_form()
        except Error as e:
            QMessageBox.critical(self, "Error", f"Error al guardar cliente:\n{e}")

    def edit_cliente(self):
        telefono = self.entry_telefono_cliente.text().strip()
        nombre = self.entry_nombre_cliente.text().strip()
        direccion = self.entry_direccion_cliente.text().strip()
        rfc = self.entry_rfc_cliente.text().strip()
        correo = self.entry_correo_cliente.text().strip()

        if not telefono or not nombre:
            QMessageBox.warning(self, "Advertencia", "Teléfono y Nombre son campos obligatorios")
            return

        try:
            cursor = self.connection.cursor()
            cursor.execute(
                "UPDATE Clientes SET nombre=%s, direccion=%s, rfc=%s, correo=%s WHERE telefono=%s",
                (nombre, direccion, rfc, correo, telefono)
            )
            self.connection.commit()
            QMessageBox.information(self, "Éxito", "Cliente actualizado correctamente")
            self.load_clientes()
        except Error as e:
            QMessageBox.critical(self, "Error", f"Error al actualizar cliente:\n{e}")

    def delete_cliente(self):
        telefono = self.entry_telefono_cliente.text().strip()

        if not telefono:
            QMessageBox.warning(self, "Advertencia", "Seleccione un cliente para eliminar")
            return

        confirm = QMessageBox.question(
            self, "Confirmar eliminación", f"¿Está seguro que desea eliminar al cliente con teléfono {telefono}?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )

        if confirm == QMessageBox.StandardButton.Yes:
            try:
                cursor = self.connection.cursor()
                cursor.execute("DELETE FROM Clientes WHERE telefono=%s", (telefono,))
                self.connection.commit()
                QMessageBox.information(self, "Éxito", "Cliente eliminado correctamente")
                self.load_clientes()
                self.clear_cliente_form()
            except Error as e:
                QMessageBox.critical(self, "Error", f"Error al eliminar cliente:\n{e}")

    def clear_cliente_form(self):
        self.entry_telefono_cliente.clear()
        self.entry_nombre_cliente.clear()
        self.entry_direccion_cliente.clear()
        self.entry_rfc_cliente.clear()
        self.entry_correo_cliente.clear()

    def load_cliente_from_table(self, row):
        self.entry_telefono_cliente.setText(self.table_clientes.item(row, 0).text())
        self.entry_nombre_cliente.setText(self.table_clientes.item(row, 1).text())
        self.entry_direccion_cliente.setText(self.table_clientes.item(row, 2).text())
        self.entry_rfc_cliente.setText(self.table_clientes.item(row, 3).text())
        self.entry_correo_cliente.setText(self.table_clientes.item(row, 4).text())

    # Métodos para Artículos
    def load_articulos(self):
        try:
            cursor = self.connection.cursor()
            cursor.execute("""
                SELECT a.codigo, a.nombre, a.precio, a.costo, a.existencia, a.unidad, c.nombre 
                FROM Articulos a
                LEFT JOIN Categoria c ON a.idcategoria = c.idcategoria
            """)
            articulos = cursor.fetchall()
            self.table_articulos.setRowCount(len(articulos))
            for row_idx, row_data in enumerate(articulos):
                for col_idx, col_data in enumerate(row_data):
                    self.table_articulos.setItem(row_idx, col_idx, QTableWidgetItem(str(col_data)))
        except Error as e:
            QMessageBox.critical(self, "Error", f"Error al cargar artículos:\n{e}")

    def save_articulo(self):
        codigo = self.entry_codigo_articulo.text().strip()
        nombre = self.entry_nombre_articulo.text().strip()
        precio = self.entry_precio_articulo.text().strip()
        costo = self.entry_costo_articulo.text().strip()
        existencia = self.entry_existencia_articulo.text().strip()
        unidad = self.entry_unidad_articulo.text().strip()
        idcategoria = self.combo_categoria_articulo.currentData()

        if not codigo or not nombre:
            QMessageBox.warning(self, "Advertencia", "Código y Nombre son campos obligatorios")
            return

        try:
            cursor = self.connection.cursor()
            cursor.execute(
                """INSERT INTO Articulos (codigo, nombre, precio, costo, existencia, unidad, idcategoria) 
                VALUES (%s, %s, %s, %s, %s, %s, %s)""",
                (codigo, nombre, float(precio) if precio else None, 
                 float(costo) if costo else None, 
                 int(existencia) if existencia else None, 
                 unidad, idcategoria)
            )
            self.connection.commit()
            QMessageBox.information(self, "Éxito", "Artículo guardado correctamente")
            self.load_articulos()
            self.clear_articulo_form()
        except Error as e:
            QMessageBox.critical(self, "Error", f"Error al guardar artículo:\n{e}")

    def edit_articulo(self):
        codigo = self.entry_codigo_articulo.text().strip()
        nombre = self.entry_nombre_articulo.text().strip()
        precio = self.entry_precio_articulo.text().strip()
        costo = self.entry_costo_articulo.text().strip()
        existencia = self.entry_existencia_articulo.text().strip()
        unidad = self.entry_unidad_articulo.text().strip()
        idcategoria = self.combo_categoria_articulo.currentData()

        if not codigo or not nombre:
            QMessageBox.warning(self, "Advertencia", "Código y Nombre son campos obligatorios")
            return

        try:
            cursor = self.connection.cursor()
            cursor.execute(
                """UPDATE Articulos SET nombre=%s, precio=%s, costo=%s, existencia=%s, unidad=%s, idcategoria=%s 
                WHERE codigo=%s""",
                (nombre, float(precio) if precio else None, 
                 float(costo) if costo else None, 
                 int(existencia) if existencia else None, 
                 unidad, idcategoria, codigo)
            )
            self.connection.commit()
            QMessageBox.information(self, "Éxito", "Artículo actualizado correctamente")
            self.load_articulos()
        except Error as e:
            QMessageBox.critical(self, "Error", f"Error al actualizar artículo:\n{e}")

    def delete_articulo(self):
        codigo = self.entry_codigo_articulo.text().strip()

        if not codigo:
            QMessageBox.warning(self, "Advertencia", "Seleccione un artículo para eliminar")
            return

        confirm = QMessageBox.question(
            self, "Confirmar eliminación", f"¿Está seguro que desea eliminar el artículo con código {codigo}?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )

        if confirm == QMessageBox.StandardButton.Yes:
            try:
                cursor = self.connection.cursor()
                cursor.execute("DELETE FROM Articulos WHERE codigo=%s", (codigo,))
                self.connection.commit()
                QMessageBox.information(self, "Éxito", "Artículo eliminado correctamente")
                self.load_articulos()
                self.clear_articulo_form()
            except Error as e:
                QMessageBox.critical(self, "Error", f"Error al eliminar artículo:\n{e}")

    def clear_articulo_form(self):
        self.entry_codigo_articulo.clear()
        self.entry_nombre_articulo.clear()
        self.entry_precio_articulo.clear()
        self.entry_costo_articulo.clear()
        self.entry_existencia_articulo.clear()
        self.entry_unidad_articulo.clear()
        self.combo_categoria_articulo.setCurrentIndex(0)

    def load_articulo_from_table(self, row):
        self.entry_codigo_articulo.setText(self.table_articulos.item(row, 0).text())
        self.entry_nombre_articulo.setText(self.table_articulos.item(row, 1).text())
        self.entry_precio_articulo.setText(self.table_articulos.item(row, 2).text())
        self.entry_costo_articulo.setText(self.table_articulos.item(row, 3).text())
        self.entry_existencia_articulo.setText(self.table_articulos.item(row, 4).text())
        self.entry_unidad_articulo.setText(self.table_articulos.item(row, 5).text())
        
        # Buscar la categoría en el combo
        categoria = self.table_articulos.item(row, 6).text()
        index = self.combo_categoria_articulo.findText(categoria)
        if index >= 0:
            self.combo_categoria_articulo.setCurrentIndex(index)

    # Métodos para Categorías
    def load_categorias(self):
        try:
            cursor = self.connection.cursor()
            cursor.execute("SELECT idcategoria, nombre FROM Categoria")
            categorias = cursor.fetchall()
            self.table_categorias.setRowCount(len(categorias))
            for row_idx, row_data in enumerate(categorias):
                for col_idx, col_data in enumerate(row_data):
                    self.table_categorias.setItem(row_idx, col_idx, QTableWidgetItem(str(col_data)))
        except Error as e:
            QMessageBox.critical(self, "Error", f"Error al cargar categorías:\n{e}")

    def save_categoria(self):
        idcategoria = self.entry_id_categoria.text().strip()
        nombre = self.entry_nombre_categoria.text().strip()

        if not idcategoria or not nombre:
            QMessageBox.warning(self, "Advertencia", "ID y Nombre son campos obligatorios")
            return

        try:
            cursor = self.connection.cursor()
            cursor.execute(
                "INSERT INTO Categoria (idcategoria, nombre) VALUES (%s, %s)",
                (int(idcategoria), nombre)
            )
            self.connection.commit()
            QMessageBox.information(self, "Éxito", "Categoría guardada correctamente")
            self.load_categorias()
            self.load_categorias_combo()  # Actualizar combos que usan categorías
            self.clear_categoria_form()
        except Error as e:
            QMessageBox.critical(self, "Error", f"Error al guardar categoría:\n{e}")

    def edit_categoria(self):
        idcategoria = self.entry_id_categoria.text().strip()
        nombre = self.entry_nombre_categoria.text().strip()

        if not idcategoria or not nombre:
            QMessageBox.warning(self, "Advertencia", "ID y Nombre son campos obligatorios")
            return

        try:
            cursor = self.connection.cursor()
            cursor.execute(
                "UPDATE Categoria SET nombre=%s WHERE idcategoria=%s",
                (nombre, int(idcategoria))
            )
            self.connection.commit()
            QMessageBox.information(self, "Éxito", "Categoría actualizada correctamente")
            self.load_categorias()
            self.load_categorias_combo()  # Actualizar combos que usan categorías
        except Error as e:
            QMessageBox.critical(self, "Error", f"Error al actualizar categoría:\n{e}")

    def delete_categoria(self):
        idcategoria = self.entry_id_categoria.text().strip()

        if not idcategoria:
            QMessageBox.warning(self, "Advertencia", "Seleccione una categoría para eliminar")
            return

        confirm = QMessageBox.question(
            self, "Confirmar eliminación", f"¿Está seguro que desea eliminar la categoría con ID {idcategoria}?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )

        if confirm == QMessageBox.StandardButton.Yes:
            try:
                cursor = self.connection.cursor()
                cursor.execute("DELETE FROM Categoria WHERE idcategoria=%s", (int(idcategoria),))
                self.connection.commit()
                QMessageBox.information(self, "Éxito", "Categoría eliminada correctamente")
                self.load_categorias()
                self.load_categorias_combo()  # Actualizar combos que usan categorías
                self.clear_categoria_form()
            except Error as e:
                QMessageBox.critical(self, "Error", f"Error al eliminar categoría:\n{e}")

    def clear_categoria_form(self):
        self.entry_id_categoria.clear()
        self.entry_nombre_categoria.clear()

    def load_categoria_from_table(self, row):
        self.entry_id_categoria.setText(self.table_categorias.item(row, 0).text())
        self.entry_nombre_categoria.setText(self.table_categorias.item(row, 1).text())

    # Métodos para Ventas
    def load_ventas(self):
        try:
            cursor = self.connection.cursor()
            cursor.execute("""
                SELECT v.ventas, v.fecha, v.importe, v.iva, v.total, c.nombre 
                FROM Ventas v
                LEFT JOIN Clientes c ON v.telefono = c.telefono
            """)
            ventas = cursor.fetchall()
            self.table_ventas.setRowCount(len(ventas))
            for row_idx, row_data in enumerate(ventas):
                for col_idx, col_data in enumerate(row_data):
                    self.table_ventas.setItem(row_idx, col_idx, QTableWidgetItem(str(col_data)))
        except Error as e:
            QMessageBox.critical(self, "Error", f"Error al cargar ventas:\n{e}")

    def save_venta(self):
        ventas = self.entry_id_venta.text().strip()
        fecha = self.date_venta.date().toString("yyyy-MM-dd")
        importe = self.entry_importe_venta.text().strip()
        iva = self.entry_iva_venta.text().strip()
        total = self.entry_total_venta.text().strip()
        telefono = self.combo_cliente_venta.currentData()

        if not ventas:
            QMessageBox.warning(self, "Advertencia", "ID Venta es un campo obligatorio")
            return

        try:
            cursor = self.connection.cursor()
            cursor.execute(
                """INSERT INTO Ventas (ventas, fecha, importe, iva, total, telefono) 
                VALUES (%s, %s, %s, %s, %s, %s)""",
                (int(ventas), fecha, 
                 float(importe) if importe else None, 
                 float(iva) if iva else None, 
                 float(total) if total else None, 
                 telefono)
            )
            self.connection.commit()
            QMessageBox.information(self, "Éxito", "Venta guardada correctamente")
            self.load_ventas()
            self.clear_venta_form()
        except Error as e:
            QMessageBox.critical(self, "Error", f"Error al guardar venta:\n{e}")

    def edit_venta(self):
        ventas = self.entry_id_venta.text().strip()
        fecha = self.date_venta.date().toString("yyyy-MM-dd")
        importe = self.entry_importe_venta.text().strip()
        iva = self.entry_iva_venta.text().strip()
        total = self.entry_total_venta.text().strip()
        telefono = self.combo_cliente_venta.currentData()

        if not ventas:
            QMessageBox.warning(self, "Advertencia", "ID Venta es un campo obligatorio")
            return

        try:
            cursor = self.connection.cursor()
            cursor.execute(
                """UPDATE Ventas SET fecha=%s, importe=%s, iva=%s, total=%s, telefono=%s 
                WHERE ventas=%s""",
                (fecha, float(importe) if importe else None, 
                 float(iva) if iva else None, 
                 float(total) if total else None, 
                 telefono, int(ventas))
            )
            self.connection.commit()
            QMessageBox.information(self, "Éxito", "Venta actualizada correctamente")
            self.load_ventas()
        except Error as e:
            QMessageBox.critical(self, "Error", f"Error al actualizar venta:\n{e}")

    def delete_venta(self):
        ventas = self.entry_id_venta.text().strip()

        if not ventas:
            QMessageBox.warning(self, "Advertencia", "Seleccione una venta para eliminar")
            return

        confirm = QMessageBox.question(
            self, "Confirmar eliminación", f"¿Está seguro que desea eliminar la venta con ID {ventas}?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )

        if confirm == QMessageBox.StandardButton.Yes:
            try:
                cursor = self.connection.cursor()
                cursor.execute("DELETE FROM Ventas WHERE ventas=%s", (int(ventas),))
                self.connection.commit()
                QMessageBox.information(self, "Éxito", "Venta eliminada correctamente")
                self.load_ventas()
                self.clear_venta_form()
            except Error as e:
                QMessageBox.critical(self, "Error", f"Error al eliminar venta:\n{e}")

    def clear_venta_form(self):
        self.entry_id_venta.clear()
        self.date_venta.setDate(QDate.currentDate())
        self.entry_importe_venta.clear()
        self.entry_iva_venta.clear()
        self.entry_total_venta.clear()
        self.combo_cliente_venta.setCurrentIndex(0)

    def load_venta_from_table(self, row):
        self.entry_id_venta.setText(self.table_ventas.item(row, 0).text())
        
        # Fecha
        fecha_str = self.table_ventas.item(row, 1).text()
        fecha = QDate.fromString(fecha_str, "yyyy-MM-dd")
        self.date_venta.setDate(fecha)
        
        self.entry_importe_venta.setText(self.table_ventas.item(row, 2).text())
        self.entry_iva_venta.setText(self.table_ventas.item(row, 3).text())
        self.entry_total_venta.setText(self.table_ventas.item(row, 4).text())
        
        # Buscar el cliente en el combo
        cliente = self.table_ventas.item(row, 5).text()
        index = self.combo_cliente_venta.findText(cliente, Qt.MatchFlag.MatchContains)
        if index >= 0:
            self.combo_cliente_venta.setCurrentIndex(index)

    # Métodos para Detalle Ventas
    def load_detalle_ventas(self):
        try:
            cursor = self.connection.cursor()
            cursor.execute("""
                SELECT dv.ventas, v.ventas, dv.codigo, a.nombre, dv.cantidad, dv.precio, dv.importe
                FROM Detalle_Ventas dv
                JOIN Ventas v ON dv.ventas = v.ventas
                JOIN Articulos a ON dv.codigo = a.codigo
            """)
            detalles = cursor.fetchall()
            self.table_detalle_ventas.setRowCount(len(detalles))
            for row_idx, row_data in enumerate(detalles):
                for col_idx, col_data in enumerate(row_data):
                    self.table_detalle_ventas.setItem(row_idx, col_idx, QTableWidgetItem(str(col_data)))
        except Error as e:
            QMessageBox.critical(self, "Error", f"Error al cargar detalles de ventas:\n{e}")

    def save_detalle_venta(self):
        ventas = self.combo_venta_detalle.currentData()
        codigo = self.combo_articulo_detalle.currentData()
        cantidad = self.entry_cantidad_detalle.text().strip()
        precio = self.entry_precio_detalle.text().strip()
        importe = self.entry_importe_detalle.text().strip()

        if not ventas or not codigo or not cantidad:
            QMessageBox.warning(self, "Advertencia", "Venta, Artículo y Cantidad son campos obligatorios")
            return

        try:
            cursor = self.connection.cursor()
            cursor.execute(
                """INSERT INTO Detalle_Ventas (ventas, codigo, cantidad, precio, importe) 
                VALUES (%s, %s, %s, %s, %s)""",
                (int(ventas), codigo, int(cantidad), 
                 float(precio) if precio else None, 
                 float(importe) if importe else None)
            )
            self.connection.commit()
            QMessageBox.information(self, "Éxito", "Detalle de venta guardado correctamente")
            self.load_detalle_ventas()
            self.clear_detalle_form()
        except Error as e:
            QMessageBox.critical(self, "Error", f"Error al guardar detalle de venta:\n{e}")

    def edit_detalle_venta(self):
        ventas = self.combo_venta_detalle.currentData()
        codigo = self.combo_articulo_detalle.currentData()
        cantidad = self.entry_cantidad_detalle.text().strip()
        precio = self.entry_precio_detalle.text().strip()
        importe = self.entry_importe_detalle.text().strip()

        if not ventas or not codigo or not cantidad:
            QMessageBox.warning(self, "Advertencia", "Venta, Artículo y Cantidad son campos obligatorios")
            return

        try:
            cursor = self.connection.cursor()
            cursor.execute(
                """UPDATE Detalle_Ventas SET cantidad=%s, precio=%s, importe=%s 
                WHERE ventas=%s AND codigo=%s""",
                (int(cantidad), float(precio) if precio else None, 
                 float(importe) if importe else None, 
                 int(ventas), codigo)
            )
            self.connection.commit()
            QMessageBox.information(self, "Éxito", "Detalle de venta actualizado correctamente")
            self.load_detalle_ventas()
        except Error as e:
            QMessageBox.critical(self, "Error", f"Error al actualizar detalle de venta:\n{e}")

    def delete_detalle_venta(self):
        ventas = self.combo_venta_detalle.currentData()
        codigo = self.combo_articulo_detalle.currentData()

        if not ventas or not codigo:
            QMessageBox.warning(self, "Advertencia", "Seleccione un detalle de venta para eliminar")
            return

        confirm = QMessageBox.question(
            self, "Confirmar eliminación", 
            f"¿Está seguro que desea eliminar el detalle de venta {ventas} - {codigo}?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )

        if confirm == QMessageBox.StandardButton.Yes:
            try:
                cursor = self.connection.cursor()
                cursor.execute(
                    "DELETE FROM Detalle_Ventas WHERE ventas=%s AND codigo=%s",
                    (int(ventas), codigo)
                )
                self.connection.commit()
                QMessageBox.information(self, "Éxito", "Detalle de venta eliminado correctamente")
                self.load_detalle_ventas()
                self.clear_detalle_form()
            except Error as e:
                QMessageBox.critical(self, "Error", f"Error al eliminar detalle de venta:\n{e}")

    def clear_detalle_form(self):
        self.combo_venta_detalle.setCurrentIndex(0)
        self.combo_articulo_detalle.setCurrentIndex(0)
        self.entry_cantidad_detalle.clear()
        self.entry_precio_detalle.clear()
        self.entry_importe_detalle.clear()

    def load_detalle_from_table(self, row):
        # Obtener IDs de la tabla
        ventas_id = self.table_detalle_ventas.item(row, 0).text()
        codigo = self.table_detalle_ventas.item(row, 2).text()
        
        # Buscar la venta en el combo
        index_venta = self.combo_venta_detalle.findData(int(ventas_id))
        if index_venta >= 0:
            self.combo_venta_detalle.setCurrentIndex(index_venta)
        
        # Buscar el artículo en el combo
        index_articulo = self.combo_articulo_detalle.findData(codigo)
        if index_articulo >= 0:
            self.combo_articulo_detalle.setCurrentIndex(index_articulo)
        
        self.entry_cantidad_detalle.setText(self.table_detalle_ventas.item(row, 4).text())
        self.entry_precio_detalle.setText(self.table_detalle_ventas.item(row, 5).text())
        self.entry_importe_detalle.setText(self.table_detalle_ventas.item(row, 6).text())

    # Métodos auxiliares para combos
    def load_categorias_combo(self):
        try:
            cursor = self.connection.cursor()
            cursor.execute("SELECT idcategoria, nombre FROM Categoria")
            categorias = cursor.fetchall()

            self.combo_categoria_articulo.clear()
            for idcat, nombre in categorias:
                self.combo_categoria_articulo.addItem(nombre, idcat)
        except Error as e:
            QMessageBox.critical(self, "Error", f"Error al cargar categorías:\n{e}")

    def load_clientes_combo(self):
        try:
            cursor = self.connection.cursor()
            cursor.execute("SELECT telefono, nombre FROM Clientes")
            clientes = cursor.fetchall()

            self.combo_cliente_venta.clear()
            for telefono, nombre in clientes:
                self.combo_cliente_venta.addItem(f"{nombre} ({telefono})", telefono)
        except Error as e:
            QMessageBox.critical(self, "Error", f"Error al cargar clientes:\n{e}")

    def load_ventas_combo(self):
        try:
            cursor = self.connection.cursor()
            cursor.execute("SELECT ventas, ventas FROM Ventas")  # Mostramos solo el ID
            ventas = cursor.fetchall()

            self.combo_venta_detalle.clear()
            for id_venta, _ in ventas:
                self.combo_venta_detalle.addItem(str(id_venta), id_venta)
        except Error as e:
            QMessageBox.critical(self, "Error", f"Error al cargar ventas:\n{e}")

    def load_articulos_combo(self):
        try:
            cursor = self.connection.cursor()
            cursor.execute("SELECT codigo, nombre FROM Articulos")
            articulos = cursor.fetchall()

            self.combo_articulo_detalle.clear()
            for codigo, nombre in articulos:
                self.combo_articulo_detalle.addItem(f"{nombre} ({codigo})", codigo)
        except Error as e:
            QMessageBox.critical(self, "Error", f"Error al cargar artículos:\n{e}")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setStyleSheet("""
        QMainWindow {
            background-color: #1e1e1e;
        }
        QLabel {
            font-size: 14px;
            color: #ffffff;
        }
        QLineEdit, QComboBox, QDateEdit {
            padding: 5px;
            font-size: 14px;
            border: 1px solid #444;
            border-radius: 4px;
            background-color: #2c2c2c;
            color: #ffffff;
        }
        QTableWidget {
            background-color: #2c2c2c;
            border: 1px solid #555;
            color: #ffffff;
        }
        QHeaderView::section {
            background-color: #444;
            color: white;
        }
    """)
    window = COMEXApp()
    window.show()
    sys.exit(app.exec())