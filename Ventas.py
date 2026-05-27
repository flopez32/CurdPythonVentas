from Conexon import CConexion  # ajusta si tu clase se llama diferente


class CVentas:

    @staticmethod
    def IngresarVentas(Nombre, Producto, Precio, Domicilio):
        try:
            conne = CConexion.ConexionBaseDeDatos()
            cursor = conne.cursor()

            sql = """
            INSERT INTO Ventas_Mes (Nombre, Producto, Precio, Domicilio)
            VALUES (?, ?, ?, ?)
            """

            valores = (Nombre, Producto, Precio, Domicilio)

            cursor.execute(sql, valores)
            conne.commit()

            conne.close()

            return True  #  éxito

        except Exception as e:
            print(" Error real:", e)
            return False  #  falló
        
    @staticmethod        
    def EliminarVenta(Id):
        
        try:
            conne = CConexion.ConexionBaseDeDatos()
            cursor = conne.cursor()

            sql = "DELETE FROM dbo.Ventas_Mes  WHERE Id = ?"

            cursor.execute(sql, (Id,))
            conne.commit()

            print("Registro eliminado correctamente")

            conne.close()

            return True

        except Exception as e:
            print(" Error al eliminar:", e)
            return False 
        
    def MostrarVenta():

        try:
            conne = CConexion.ConexionBaseDeDatos()
            cursor = conne.cursor()
            cursor.execute("select * from Ventas_Mes")
            MiResultado = cursor.fetchall()
            conne.commit()
            conne.close()
            return MiResultado  #  éxito

        except Exception as e:
            print(" Error al mostrar datos:", e)
            
                