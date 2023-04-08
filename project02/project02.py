try:
    import io
    import pandas as pd
    import numpy as np
    import boto3
    import psycopg2
    import configparser
    import mysql.connector as mysqlC
    import pymysql
    print("Carga de librerias.")
except Exception as ex:
    print("Error en carga de librerias.")
    print(ex)

try:
    config = configparser.ConfigParser()
    config.read('config/escec.cfg')
    print('Se obtiene config')
except Exception as ex:
    print("Error al obtener archivo de configuracion.")
    print(ex)

try:
    RDS_HOST = 'db-rent-cars.chf84lio5m7c.us-east-1.rds.amazonaws.com'
    mysql_driver = f"""mysql+pymysql://{config.get('RDS_MYSQL', 'DB_USER')}:{config.get('RDS_MYSQL', 'DB_PASSWORD')}@{RDS_HOST}:{config.get('RDS_MYSQL', 'DB_PORT')}/{config.get('RDS_MYSQL', 'DB_NAME')}"""  
    print('Conexion con RDS Exitosa..!!')
except Exception as ex:
    print("Error al conectar con RDS.")
    print(ex)

try:
    s3 = boto3.resource(
        service_name = 's3',
        region_name = 'us-east-1',
        aws_access_key_id = config.get('IAM', 'ACCESS_KEY'),
        aws_secret_access_key = config.get('IAM', 'SECRET_ACCESS_KEY')
    )
    S3_BUCKET_NAME = 'bucket-23000712'
    print('Conexion con S3 Exitosa..!!')
except Exception as ex:
    print("Error al conectar con S3.")
    print(ex)

try:
    file = s3.Bucket(S3_BUCKET_NAME).Object('dim_date.xlsx').get()
    data = file['Body'].read()
    df_dim_date = pd.read_excel(io.BytesIO(data), engine='openpyxl')
    df_dim_date = df_dim_date[['date key','full date','day of week','day num in month',	'day name','quarter','year']]
    df_dim_date = df_dim_date.rename(columns={'date key':'date_key','full date':'full_date','day of week':'day_of_week','day num in month':'day_num_in_month',	'day name':'day_name','quarter':'quarter','year':'year'})
    print('Creacion de df_dim_date Exitosa..!!')
except Exception as ex:
    print("No es un archivo.")
    print(ex)

try:
    file = s3.Bucket(S3_BUCKET_NAME).Object('dim_state.xlsx').get()
    data = file['Body'].read()
    df_state = pd.read_excel(io.BytesIO(data), engine='openpyxl')
except Exception as ex:
    print("No es un archivo.")
    print(ex)

try:
    sql_query = 'SELECT * FROM location;'
    df_location = pd.read_sql(sql_query, mysql_driver)
    df_location.head()
    df_dim_location = df_location.merge(df_state, 
                                                    left_on='state',
                                                    right_on='id',
                                                    how='left',
                                                    suffixes=('_loc','_sta'))
    df_dim_location.drop(['state_loc', 'zipcode', 'id_sta'], axis=1, inplace=True)
    df_dim_location.rename(columns={'state_sta': 'state'}, inplace=True)
    print('Creacion de df_dim_location Exitosa..!!')
except Exception as ex:
    print("Error al obtener df_dim_location.")
    print(ex)

try:
    sql_query = 'SELECT * FROM customer;'
    df_dim_customer = pd.read_sql(sql_query, mysql_driver)
    df_dim_customer['name'] = df_dim_customer['first_name'] + ' ' + df_dim_customer['last_name']
    df_dim_customer.drop(['dob', 'email', 'phone', 'first_name', 'last_name'], axis=1, inplace=True)
    df_dim_customer = df_dim_customer.reindex(columns=['id', 'name', 'driver_license_number'])
    df_dim_customer.rename(columns={'driver_license_number': 'driver_license'}, inplace=True)
    print('Creacion de df_dim_customer Exitosa..!!')
except Exception as ex:
    print("Error al obtener df_dim_customer.")
    print(ex)

try:
    sql_query = 'SELECT * FROM vehicle;'
    df_vehicle = pd.read_sql(sql_query, mysql_driver)

    sql_query = 'SELECT * FROM vehicle_type;'
    df_vehicle_type = pd.read_sql(sql_query, mysql_driver)


    df_dim_vehicle = df_vehicle_type.merge(df_vehicle, 
                                                    left_on='id',
                                                    right_on='vehicle_type_id',
                                                    how='left',
                                                    suffixes=('_type','_veh'))
    df_dim_vehicle.drop(['id_veh', 'vehicle_type_id', 'current_location_id'], axis=1, inplace=True)
    print('Creacion de df_dim_vehicle Exitosa..!!')
except Exception as ex:
    print("Error al obtener df_dim_vehicle.")
    print(ex) 

try:
    sql_query = 'SELECT * from fuel_option;'
    df_dim_fuel = pd.read_sql(sql_query, mysql_driver)
    df_dim_fuel.drop(['description'], axis=1, inplace=True)
    print('Creacion de df_dim_fuel Exitosa..!!')
except Exception as ex:
    print("Error al obtener df_dim_fuel.")
    print(ex) 

try:
    sql_query = 'SELECT * FROM rental;'
    df_fact_rental = pd.read_sql(sql_query, mysql_driver)
    df_fact_rental['start_date_key'] = pd.to_datetime(df_fact_rental['start_date'], format='%Y-%m-%d').dt.strftime('%Y%m%d').astype(int)
    df_fact_rental['end_date_key'] = pd.to_datetime(df_fact_rental['end_date'], format='%Y-%m-%d').dt.strftime('%Y%m%d').astype(int)
    df_fact_rental.drop(['start_date', 'end_date'], axis=1, inplace=True)
    print('Creacion de df_fact_rental Exitosa..!!')
except Exception as ex:
    print("Error al obtener df_fact_rental.")
    print(ex) 

try:
    df_rental = df_fact_rental.merge(df_dim_customer, left_on='customer_id', right_on='id', how='left', suffixes=('_rental','_customer'))
    df_rental = df_rental.merge(df_dim_vehicle, left_on='vehicle_type_id', right_on='id_type', how='left', suffixes=('_rental','_veh'))
    df_rental = df_rental.merge(df_dim_fuel, left_on='fuel_option_id', right_on='id', how='left', suffixes=('_rental','_fuel'))
    df_rental = df_rental.merge(df_dim_location, left_on='pickup_location_id', right_on='id_loc', how='left', suffixes=('_rental','_pick'))
    df_rental = df_rental.merge(df_dim_location, left_on='drop_off_location_id', right_on='id_loc', how='left', suffixes=('_pick','_drop'))
    df_rental = df_rental.merge(df_dim_date, left_on='start_date_key', right_on='date_key', how='left', suffixes=('_rental','_start'))
    df_rental = df_rental.merge(df_dim_date, left_on='end_date_key', right_on='date_key', how='left', suffixes=('_start','_end'))


    df_rental.drop(['customer_id', 'vehicle_type_id', 
                    'fuel_option_id', 'pickup_location_id', 
                    'drop_off_location_id', 'start_date_key', 
                    'end_date_key', 'id_customer',
                    'id_type', 'id', 'id_loc_pick',
                    'id_loc_drop', 'date_key_start',
                    'date_key_end'
                ], axis=1, inplace=True)


    df_rental = df_rental.reindex(columns=['id_rental', 'name_rental', 'driver_license',
                                        'brand',	'model', 'model_year',	
                                        'mileage', 'color', 'name_veh', 'rental_value',	
                                        'name', 'street_address_pick', 'city_pick', 'state_pick',	
                                        'full_date_start', 'day_of_week_start', 'day_num_in_month_start',	
                                        'day_name_start', 'quarter_start', 'year_start',	
                                        'street_address_drop', 'city_drop', 'state_drop',	
                                        'full_date_end',	'day_of_week_end', 'day_num_in_month_end', 
                                        'day_name_end', 'quarter_end', 'year_end' 
                                        ])

    df_rental.rename(columns={'name_rental': 'name_customer', 
                                    'driver_license': 'license_customer',
                                    'brand': 'brand_vehicle',	
                                    'model': 'model_vehicle', 
                                    'model_year': 'model_year_vehicle',	
                                    'mileage': 'mileage_vehicle', 
                                    'color': 'color_vehicle', 
                                    'name_veh': 'type_vehicle', 	
                                    'name': 'fuel_option', 
                                    'street_address_pick': 'street_address_start', 
                                    'city_pick': 'city_start', 
                                    'state_pick': 'state_start',	
                                    'full_date_start': 'date_start', 	
                                    'street_address_drop': 'street_address_end', 
                                    'city_drop': 'city_end', 
                                    'state_drop': 'state_end' ,	
                                    'full_date_end': 'date_end'
                                }, inplace=True)
    print('Modificaciones a df_rental se realizaron de manera exitosa..!!')
except Exception as ex:
    print("Error al modificar df_rental.")
    print(ex) 

try:
    print('Inicia carga de df_rental a S3..!!')
    df_rental.to_excel('data/df_rental.xlsx', index=False)

    s3.Bucket(S3_BUCKET_NAME).upload_file('data/df_rental.xlsx', 'df_rental.xlsx')
    print('Carga de df_rental a S3 realizada de manera exitosa..!!')
except Exception as ex:
    print("Error al cargar df_rental.")
    print(ex)

