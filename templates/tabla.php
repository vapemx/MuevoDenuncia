<!DOCTYPE html>
<html>
<head>
  <title>Tabla de Denuncias</title>
  <h2>Mis Denuncias</h2>
  <style>
    * {
      margin: 0;
      padding: 0;
      box-sizing: border-box;
    }

    body {
      background: #0f0c29;
      background: -webkit-linear-gradient(to right, #24243e, #302b63, #0f0c29);
      background: linear-gradient(to right, #24243e, #302b63);
      text-align: center;
      font-family: sans-serif;
    }

    .denuncias {
      margin-top: 20px;
      width: 80%;
      max-width: 800px;
      margin: auto;
      background-color: #fff;
      border-radius: 5px;
      box-shadow: 0 2px 5px rgba(0, 0, 0, 0.3);
    }

    .denuncias thead {
      background-color: #4286f4;
      color: #fff;
    }

    .denuncias th,
    .denuncias td {
      padding: 10px;
      text-align: center;
    }

    .denuncias tbody tr:nth-child(even) {
      background-color: #f2f2f2;
    }
    h2 {
      color: #fff;
  font-size: 36px;
  text-align: center;
  margin-top: 40px;
  margin-bottom: 20px;
}
  </style>
</head>
<body>
  <form>
    <input type="text" name="address" placeholder="Ingrese su address" required>
    <button type="submit" name="revisar">Revisar</button> <br> <br> 
  </form>
  
  <?php
    include 'getconex.php'; // Incluir el archivo POSTconex.php para establecer la conexión

      $address = $_GET['address']; // Obtener el valor ingresado por el usuario en el campo de dirección
      
      // Realizar la consulta SQL para obtener los datos de la tabla "complaints" basados en la dirección ingresada
      $query = "SELECT signers, vehicle_reported, incident_date, municipio, street, reference, complaint, resolved, complaint_hash FROM complaints WHERE signers = '$address'";
      
      $result = sqlsrv_query($conectar, $query); // Ejecutar la consulta
      
      // Verificar si se obtuvieron resultados
      if ($result === false) {
        die(print_r(sqlsrv_errors(), true)); // Mostrar errores en caso de que ocurran
      }
      
      // Crear la tabla HTML con los encabezados y los datos de las denuncias
      $table = '<table class="denuncias">';
      $table .= '<thead><tr><th>Address</th><th>Vehiculo Reportado</th><th>Fecha De Incidente</th><th>Municipio</th><th>Calle</th><th>Referencia</th><th>Queja</th><th>Resuelta</th><th>HASH Denuncia</th></tr></thead>';
      $table .= '<tbody>';
      
      // Recorrer los resultados y agregar cada fila a la tabla
      while ($row = sqlsrv_fetch_array($result, SQLSRV_FETCH_ASSOC)) {
        $table .= '<tr>';
        $table .= '<td>'.$row['signers'].'</td>';
        $table .= '<td>'.$row['vehicle_reported'].'</td>';
        $table .= '<td>'.$row['incident_date']->format('Y-m-d').'</td>';
        $table .= '<td>'.$row['municipio'].'</td>';
        $table .= '<td>'.$row['street'].'</td>';
        $table .= '<td>'.$row['reference'].'</td>';
        $table .= '<td>'.$row['complaint'].'</td>';
        $table .= '<td>'.$row['resolved'].'</td>';
        $table .= '<td>'.$row['complaint_hash'].'</td>';
        $table .= '</tr>';
      }
      
      $table .= '</tbody></table>';
      
      // Liberar recursos
      sqlsrv_free_stmt($result);
      
      // Cerrar la conexión
      sqlsrv_close($conectar);
    
    ?>
</body>
</html>
