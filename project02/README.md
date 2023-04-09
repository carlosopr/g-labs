# Ingeniería de datos con Python

## Introducción

Este proyecto consiste en el desarrollo de un pipeline de ingeniería utilizando Python, SQL y AWS. El objetivo del proyecto es procesar y analizar datos de diversas fuentes y proporcionar informes útiles para la toma de decisiones.

Se espera que el pipeline de ingeniería de datos sea capaz de procesar grandes cantidades de datos, limpiarlos y transformarlos en un modelo de datos que permita responder a preguntas de análisis de manera eficiente. Además, se espera que el proyecto incluya un diseño robusto y escalable que permita el manejo de los datos de manera efectiva y una documentación clara que permita a otros desarrolladores entender y mantener el código desarrollado.

## Scope

El alcance del proyecto es desarrollar un pipeline de ingeniería de datos utilizando Python, SQL y AWS. El objetivo es procesar y analizar datos de diferentes fuentes, incluyendo una base de datos alojada en un RDS de AWS y un archivo CSV almacenado en un bucket de S3 de AWS.

Para este proyecto, se utilizarán tres fuentes de datos diferentes:

1. Una base de datos alojada en un RDS de AWS: Esta base de datos proporcionará información en tiempo real que será utilizada para el análisis de los datos. Para acceder a la base de datos, se utilizará la librería mysql.connector de Python.
2. Archivo CSV con información histórica: Este archivo se encuentra almacenado en un bucket de S3 de AWS. El archivo CSV será utilizado para alimentar las dimensiones del modelo de datos. Para acceder al archivo, se utilizará la librería boto3 de Python.
3. Archivos de proyecto: El proyecto utiliza scripts de Python que contienen funciones para el procesamiento de datos, archivos de configuración, etc. 


## Exploración

El proyecto está basado en un conjunto de datos sobre rentas de vehículos de un negocio en 2018. En general, el caso de estudio permitirá analizar la demanda de rentas de vehículos, patrones de uso y preferencias de los clientes, así como para evaluar el rendimiento de la flota de vehículos y la rentabilidad del negocio de alquiler de vehículos.


El dataset final cuenta con los siguientes campos:

| Campo                | Descripción                                          |
|----------------------|------------------------------------------------------|
| id_rental            | clave única que identifica cada renta                |
| name_customer        | nombre completo del cliente                          |
| license_customer     | número de licencia de conducir del cliente           |
| brand_vehicle        | marca del vehículo                                    |
| model_vehicle        | modelo del vehículo                                   |
| model_year_vehicle   | año del modelo del vehículo                           |
| mileage_vehicle      | kilometraje del vehículo                              |
| color_vehicle        | color del vehículo                                    |
| type_vehicle         | tipo del vehículo                                     |
| rental_value         | valor de la renta                                     |
| fuel_option          | tipo de combustible utilizado en el vehículo          |
| street_address_start | dirección de inicio de la renta                       |
| city_start           | ciudad donde inició la renta                           |
| state_start          | estado donde inició la renta                           |
| date_start           | fecha de inicio de la renta                            |
| day_of_week_start    | día de la semana en que inició la renta                |
| day_num_in_month_start| número del día del mes en que inició la renta         |
| day_name_start       | nombre del día en que inició la renta                  |
| quarter_start        | trimestre en el que inició la renta                    |
| year_start           | año en que inició la renta                             |
| street_address_end   | dirección de fin de la renta                           |
| city_end             | ciudad donde finalizó la renta                         |
| state_end            | estado donde finalizó la renta                         |
| date_end             | fecha de fin de la renta                               |
| day_of_week_end      | día de la semana en que finalizó la renta              |
| day_num_in_month_end  | número del día del mes en que finalizó la renta       |
| day_name_end         | nombre del día en que finalizó la renta                |
| quarter_end          | trimestre en el que finalizó la renta                  |
| year_end             | año en que finalizó la renta                           |



## Modelo de datos 

Para este proyecto se ha optado por una estructura de data warehouse ya que permiten una fácil comprensión y análisis de los datos relacionados con la renta de vehículos. Las dimensiones elegidas son lo suficientemente amplias para proporcionar información relevante para el análisis, como la fecha y la ubicación del alquiler, y permiten una segmentación efectiva de los datos.

La tabla de hechos se centra en la información esencial relacionada con la transacción de alquiler, incluyendo información sobre el cliente, el vehículo, el tipo de combustible, la ubicación de recogida y entrega, y la fecha de inicio y finalización del alquiler. Esta estructura permite el análisis de diferentes aspectos de la transacción de alquiler, como la frecuencia de alquiler, los vehículos más populares y la ubicación de recogida y entrega más común.

A continuación se presentan las dimensiones, seguida de la tabla de hechos para el dataset mostrado en el inciso anterior:

### Dimensión de tiempo
La dimensión de tiempo se define como una tabla que contiene información sobre el tiempo en la que se realizó la renta de un vehículo. Los campos que se pueden incluir en esta dimensión son:

| Campo           | Descripción                                                     |
|----------------|-----------------------------------------------------------------|
| date_key        | Clave única que identifica cada fecha en el formato YYYYMMDD    |
| full_date       | Fecha completa en formato YYYY-MM-DD                            |
| day_of_week     | Número del día de la semana (1=Lunes, 2=Martes, etc.)            |
| day_num_in_month| Número del día dentro del mes (1-31)                             |
| day_name        | Nombre del día de la semana (Lunes, Martes, etc.)                |
| quarter         | Número del trimestre (1-4)                                      |
| year            | Año completo (YYYY)                                             |

### Dimensión geográfica
La dimensión geográfica se basa en los siguientes campos:

| Campo           | Descripción                                                     |
|----------------|-----------------------------------------------------------------|
| id       | Identificador único de la ubicación geográfica    |
| state       | Estado o provincia donde se encuentra la ubicación geográfica       |

### Dimensión de cliente
Esta dimensión permite analizar la información de alquiler de vehículos por cliente, identificar los patrones de alquiler por cliente, así como también hacer análisis de rentabilidad por cliente.

La dimensión de cliente puede ser definida por los siguientes campos:

| Campo           | Descripción                                             |
|----------------|---------------------------------------------------------|
| id             | Clave única que identifica cada cliente                  |
| name           | Nombre completo del cliente                              |
| driver_license | Número de licencia de conducir del cliente                |


### Dimensión de vehículo
La dimensión de vehículo describe los atributos de cada vehículo en el sistema de renta de vehículos. A continuación se presenta una descripción de los campos que forman parte de esta dimensión:

| Campo                  | Descripción                                                                 |
|------------------------|-----------------------------------------------------------------------------|
| id                     | clave única que identifica cada vehículo                                      |
| brand                  | marca del vehículo                                                           |
| model                  | modelo del vehículo                                                          |
| model_year             | año del modelo del vehículo                                                   |
| mileage                | kilometraje del vehículo                                                      |
| color                  | color del vehículo                                                            |
| vehicle_type_id        | clave foránea que hace referencia a la tabla de tipos de vehículos            |
| current_location_id    | clave foránea que hace referencia a la tabla de ubicaciones actuales del vehículo |

### Dimensión de Tipo de Combustible
La dimensión de tipo de combustible tiene los siguientes campos:

| Campo | Descripción                                      |
|-------|--------------------------------------------------|
| id    | Clave única que identifica cada tipo de combustible |
| name  | Nombre del tipo de combustible                    |


### Tabla de hechos
Esta tabla de hechos permite analizar diversos aspectos relacionados con la renta de vehículos, como la demanda por tipo de vehículo, opciones de combustible, ubicaciones de recogida y devolución, así como la duración de las rentas y la frecuencia de las mismas. Al cruzar la información de la tabla de hechos con las dimensiones correspondientes, es posible generar diferentes reportes y análisis para tomar decisiones estratégicas respecto a la oferta de vehículos y ubicaciones de recogida y devolución, entre otros.

La tabla de hechos para este proyecto contiene los siguientes campos:

* **id:** clave única que identifica cada registro en la tabla de hechos.
* **customer_id:** clave foránea que relaciona la tabla de hechos con la dimensión de clientes, indicando el cliente que realizó la renta del vehículo.
* **vehicle_type_id:** clave foránea que relaciona la tabla de hechos con la dimensión de tipos de vehículos, indicando el tipo de vehículo rentado.
* **fuel_option_id:** clave foránea que relaciona la tabla de hechos con la dimensión de opciones de combustible, indicando la opción de combustible elegida para el vehículo rentado.
* **pickup_location_id:** clave foránea que relaciona la tabla de hechos con la dimensión de ubicaciones, indicando la ubicación de recogida del vehículo.
* **drop_off_location_id:** clave foránea que relaciona la tabla de hechos con la dimensión de ubicaciones, indicando la ubicación de devolución del vehículo.
* **start_date_key:** clave foránea que relaciona la tabla de hechos con la dimensión de tiempo, indicando la fecha y hora de inicio de la renta.
* **end_date_key:** clave foránea que relaciona la tabla de hechos con la dimensión de tiempo, indicando la fecha y hora de fin de la renta.


## Procesamiento

Se creo el script `project02.py` que se utiliza para cargar datos de diferentes fuentes en un data warehouse, utilizando librerías como pandas, boto3, psycopg2, mysql.connector y pymysql. El script comienza leyendo un archivo de configuración, estableciendo la conexión con un RDS de Amazon Web Services y conectándose a un bucket de S3. A continuación, carga diferentes archivos excel de S3, realiza consultas SQL en una base de datos MySQL y crea dataframes de pandas que se utilizan para crear tablas dimensionales y una tabla de hechos en el data warehouse. Finalmente, se utiliza la librería sqlalchemy para cargar los dataframes en el data warehouse utilizando el lenguaje SQL. El objetivo principal del script es cargar datos de diferentes fuentes en el data warehouse de manera automatizada.


## Analítica

Derivado de la carga y transformaciones realizada, se presenta el análisis sobre la información obtenida con base en los siguientes cuestionamientos:

1. **¿Cuántos vehículos de cada marca han sido rentados?**
De acuerdo a la información registrada, se tiene que las marcas Chevrolet, Hyundai y Mitsubishi lideran el número de rentas en 2018. 

| brand_vehicle | model_vehicle | type_vehicle | counts |
| --- | --- | --- | ---:|
| Chevrolet | Cruze | Intermediate | 99 |
| Hyundai | Elantra | Intermediate | 99 |
| Mitsubishi | Mirage | Economy | 117 |
| Nissan | Versa | Economy | 117 |
| Toyota | RAV4 | Economy SUV | 112 |
| Volkswagen | Jetta | Standard | 110 |


2. **¿Cuál es el promedio de kilometraje de los vehículos rentados por tipo de vehículo?**
Según la información registrada, el tipo de vehículo **Economy** presenta el mayor kilometraje por tipo de vehículo en 2018. 

| type_vehicle | kilómetros |
|--------------|-----------:|
| Economy      | 60910.0   |
| Economy SUV  | 12566.0   |
| Intermediate | 40637.5   |
| Standard     | 2032.0    |


3. **¿Cuáles son los días de la semana con la mayor y menor demanda de alquiler de vehículos?**
Según la información suministrada, el día con mayor número de rentas es el Lunes.


| day_name_start   |   frequency |
|:-----------------|------------:|
| Thursday         |          76 |
| Sunday           |          86 |
| Tuesday          |          89 |
| Friday           |          91 |
| Wednesday        |          98 |
| Saturday         |         105 |
| Monday           |         109 | 

4. **¿Cuál es el mes que registra mayor número de rentas?**
Durante el 2018, el mes que presentó el mayor número de rentas fue julio. Se presenta la distribución a continuación.

| date_start | counts |
|------------|-------:|
| 2018-01    | 57     |
| 2018-02    | 60     |
| 2018-03    | 53     |
| 2018-04    | 31     |
| 2018-05    | 48     |
| 2018-06    | 70     |
| 2018-07    | 72     |
| 2018-08    | 54     |
| 2018-09    | 47     |
| 2018-10    | 56     |
| 2018-11    | 56     |
| 2018-12    | 23     |

5. **¿Cuáles son las 5 ciudades más populares para rentar vehículos?**
De acuerdo a la información obtenida, el top 5 de ciudades para rentar vehículos son:

| city       | count |
|------------|-------|
| Washington | 101   |
| Fort Worth | 100   |
| Dallas     | 100   |
| Seattle    | 98    |
| New York   | 89    |


6. **¿Cuál es el porcentaje de rentas con opción de combustible en el total de rentas?**
Para el caso de la información registrada en 2018, la opción Pre-pay option presenta mayor frecuencia en las rentas.

|     fuel_option    |   counts  |
|-------------------|---------:|
|       Pre-pay        | 34.097859 |
|     Self-Service     | 33.639144 |
|        Market        | 32.262997 |


7. **¿Cuánto tiempo en promedio duran las rentas de vehículos?**
Según la data histórica de 2018, el promedio de días de renta de vehículos fue de **8 días**.

