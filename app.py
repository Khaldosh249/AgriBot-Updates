from flask import Flask, render_template, request, redirect, url_for, flash , send_from_directory , send_file
# from flask_jwt_extended import JWTManager, jwt_required, create_access_token, get_jwt_identity

from openai_analyze import openai_function

from animal_func import weather_forecast_to_question_animal
from crop_func import weather_forecast_to_question_crop

from weather_forecasting import wether_forecast

import creatTablePDF



from io import BytesIO


app = Flask(__name__)


@app.route('/api/v1/animals_check', methods=['GET'])
def animals():
    request_json = request.get_json()
    
    res = openai_function(weather_forecast_to_question_animal(wether_forecast(request_json['latitude'], request_json['longitude']) , request_json['grasses'] , request_json['animals']))
    return {
        'msg':res
        }



@app.route('/api/v1/crops_check', methods=['GET'])
def crop():
    request_json = request.get_json()
    qus = weather_forecast_to_question_crop(wether_forecast(request_json['latitude'], request_json['longitude']) , request_json['soil_quality'] , request_json['crop_rotation'] , request_json['irrigation_type'] , request_json['water_retention'] , request_json['crop_type'])
    res = openai_function(qus)
    print(qus)
    return {
        'msg':res
        }

@app.route('/download_weather_forecast', methods=['POST' , 'GET'])
def download_weather_forecast():
    if request.method == 'POST':
        lat = request.form.get('lat')
        lon = request.form.get('long')
        byt = creatTablePDF.make_pdf_table(wether_forecast(lat, lon))
        # return send_from_directory(directory='.', path='weather_forecasting.pdf')
        return send_file(BytesIO(byt) , download_name= 'weather_forecasting.pdf' , as_attachment=True)
    else:
        return render_template('download_forecasting.html')



@app.route('/index', methods=['GET' , 'POST'])
def index():
    chech = False
    if request.method == 'POST':
        lat = request.form['lat']
        lon = request.form['long']
        soil_quality = request.form.get('soil_quality')
        crop_rotation = request.form.get('crop_rotation')
        irrigation_type = request.form.get('irrigation_type')
        water_retention = request.form.get('water_retention')
        crop_type = request.form.get('crop_type')
        weather = wether_forecast(lat, lon)
        days = weather['hourly']['time']
        temp = weather['hourly']['temperature_2m']
        res = openai_function(weather_forecast_to_question_crop( weather , soil_quality , crop_rotation , irrigation_type , water_retention , crop_type))
        return render_template('home.html' , res=res , days = days , temp = temp , check=True)
    else:
        return render_template('home.html' , res='Results !' , check=chech)


@app.route('/statistics', methods=['GET' , 'POST'])
def statistics():
    check = False
    if request.method == 'POST':
        lat = request.form.get('lat')
        lon = request.form.get('long')
        res = wether_forecast(lat, lon)
        days = res['hourly']['time']
        temp = res['hourly']['temperature_2m']
        return render_template('statistics.html' , days=days , temp=temp , check=True)
    else:
        return render_template('statistics.html' , check=check)




@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


""" if __name__ == '__main__':
    app.run(debug=True , port=5005) """