import requests
import pandas as pd
import psycopg2
import traceback

values=[]
cordinates=[(12.7844,77.7473),(12.7937,77.7126),(12.7663,77,7161),(12.7239,77.6826)]
for cor in cordinates:

        url="https://api.openweathermap.org/data/2.5/weather"

        param= {"lat":cor[0],
        "lon":cor[1],
        "appid":"a5b6f1a86b788fcaea34d39e62510a3b"}

        response=requests.get(url,params=param)
        data=response.json()

        if data['cod']==200:
                record={'weather_id':data['id'],
                'city_name':data['name'],
                'country_code':data['sys']['country'],
                'latitude':data['coord']['lat'],
                'longitude':data['coord']['lon'],
                'weather_main':data['weather'][0]['main'],
                'weather_description':data['weather'][0]['description'],
                'weather_icon':data['weather'][0]['icon'],
                'temperature':data['main']['temp'],
                'feels_like':data['main']['feels_like'],
                'temp_min':data['main']['temp_min'],
                'temp_max':data['main']['temp_max'],
                'pressure':data['main']['pressure'],
                'humidity':data['main']['humidity'],
                'sea_level':data['main']['sea_level'],
                'ground_level':data['main']['grnd_level'],
                'visibility':data['visibility'],
                'wind_speed':data['wind']['speed'],
                'wind_degree':data['wind']['deg'],
                'wind_gust':data['wind']['gust'],
                'cloud_percentage':data['clouds']['all'],
                'api_timestamp':data['dt'],
                'timezone_offset':data['timezone'],
                'sunrise':data['sys']['sunrise'],
                'sunset':data['sys']['sunset'],
                }
                values.append(record)


df=pd.DataFrame(values)
#print(df)
data=[tuple(row) for row in df.to_numpy() ]
if not df.empty:
        try:
                connection=psycopg2.connect(
                host="localhost",
                    port="5432",
                    database="postgres",
                    user="postgres",
                    password="Chandra&2001"
                )
                cur = connection.cursor()
                if cur.closed == 0:
                        print("Connected successfully")


                        cur.executemany(
                            """
                            INSERT INTO public.weather_staging(weather_id,city_name,country_code,latitude,longitude,weather_main,weather_description,weather_icon,temperature,feels_like,	temp_min,	temp_max,	pressure,	humidity,	sea_level,	ground_level,	visibility,	wind_speed,	wind_degree	,wind_gust,cloud_percentage,	api_timestamp,	timezone_offset,	sunrise,sunset)
                            VALUES (%s, %s, %s,%s,%s,%s, %s, %s,%s,%s,%s, %s, %s,%s,%s,%s, %s, %s,%s,%s,%s, %s, %s,%s,%s)
                            """,
                                data
                        )
                        connection.commit()
                        cur.execute("CALL load_current_day_data_to_tables();")
                        connection.commit()
                        print ("Data has been loaded sucessfully to all the child tables")

        except Exception as e:
                    print("Connection failed:", e)

                    traceback.print_exc()

        else:
                print("Sucessfully loaded the data to the database table")
        finally:
                if cur.closed == 0:
                        cur.close()
                        connection.close()
                if cur.closed != 0:
                                print("Connection is closed")




