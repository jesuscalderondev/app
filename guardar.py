import sqlite3

base = sqlite3.connect('database.db')
cur = base.cursor()
query = ("""insert into usuario(
    usuario, nombre, sexo, clave, ventas, cargo) values(?,?,?,?,?,?)
    """)
cur.execute(query, ('luisa', 'Luisa Guardiola', 'Femenino', '2023', 0, 'Administrador'))
base.commit()
base.close()
print('agregado')