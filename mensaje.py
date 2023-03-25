from funciones import create_table_productos, get_db, limpiar_carrito


create_table_productos()


Productos = [
('Salchipapa Grande', 9000),
('Chory Buty (Salchipapa)', 12000),
('Salchipollo', 14000),
('Suiza (Salchipapa)', 13000),
('Ranchera Personal(Salchipapa)',15000),
('Suizi Pollo (Salchipapa)', 17000),
('Zuisi Carne (Salchipapa)', 16000),
('Ranchi Pollo (Salchipapa)', 16000),
('Ranchi Carne (Salchipapa)', 16000), 
('Bacana (Salchipapa)', 20000),
('Super Bacana (Salchipapa)', 30000),
('Bacana Familiar (Salchipapa)', 35000), 
('Bacana Extra Familiar (Salchipapa)', 45000),
('Mega Bacana (Salchipapa)', 55000),
('Bacana Big Max (Salchipapa)', 65000), 
('Chory Buty (Patacon)', 12000),
('Pollo (Patacon)', 13000),
('Carne (Patacon)', 13000),
('Super Bacano', 18000),
('Chory Buty (Arepa)', 13000),
('Pollo (Arepa)', 14000),
('Carne (Arepa)', 14000),
('Super Bacana (Arepa)', 20000),
('Chorizos + Bollo + Ensalada', 5000),
('Alas BBQQ', 10000),
('Chicharron con Yuca', 12000),
('Jugo en angua', 5000),
('Jugo en Leche', 6000),
('Sandwich Sencillo', 9000),
('Sandwich POllo', 12000),
('Sandwich Ranchero', 12000),
('Sandwich Carne', 13000),
('Sandwich Suizo', 15000),
('Sandwich Mixto', 16000),
('Sandwich Super Bacano', 20000),
('Desgranado Sencillo', 10000),
('Desgranado Ranchero', 13000),
('Desgranado Pollo', 14000),
('Desgranado Lomo de cerdo', 15000),
('Desgranado Mixto', 18000), 
('Pechuga A La Plancha', 14000),
('Carne A La Plancha', 15000),
('Lomo De Cerdo', 16000),
('Chuleta', 17000),
('Super Bacano (Asado)', 24000),
('Hamburguesa de carne', 10000),
('Hamburguesa De Pollo', 12000),
('Hamburguesa de Lomo De Cerdo', 14000),
('Hamburguesa De Doble carne', 16000),
('Hamburguesa Mixta', 17000),
('Hamburguesa Super Bacana', 20000),
('Perro Sencillo Grande', 5000),
('Perro Ranchero Grande', 6000),
('Buty Perro', 8000),
('Chory Perro', 8000),
('Perro Zuiso', 12000),
('Perro Super Bacano', 18000),
('Maiz', 3000),
('Queso Mozarela', 4000),
('Porcion De Papas A La Francesa', 5000), 
('Extra de Carne, Pechuga O Lomo de Cerdo', 5000),
('Combo de 4 Perros', 10000),
('Dos Desgranados Rancheros', 20000),
('Salchipapa Sencilla Grande + Hamburguesa de Carne + Perro Sencillo Grande', 20000),
('Coca Cola Personal', 3000),
('Coca Cola 1.5L', 6000),
('Hit Litro', 4000),
('Postobón Personal', 2000),
('Postobón 1.5L', 5000),
('Jugo Pulpa Personal', 3000),
('Soda Personal', 3000),
('Coca Cola 3L', 8000),
('Econolitro', 3000),
('Sporade', 3000),
('Mr Tee', 3000),
('Volt', 3000),
('Speed Max', 2000),
('Agua', 1000),
('Agua Con Gas', 1000),
('Big Cola Personal', 2000),
('Big Cola Litro', 3000),
('Budweiser', 4000),
('Corona', 4000),
('Club Colombia', 5000),
('Cifrut Personal', 3000),
('Hatsu', 3000),
('Adicional Papas Francesas', 2000)
]


def registrar_producto(nombre, valor):
    db = get_db()
    cur = db.cursor()
    query= "insert into productos(nombre, valor) values(?,?)"
    valorf = valor/1000
    cur.execute(query, (nombre, valorf))
    print(f'Registrado {nombre} con un precio de {valorf}')
    db.commit()
    db.close()


for i in Productos:
    registrar_producto(i[0], i[1])