from deep_translator import GoogleTranslator
from flask import Flask, request, jsonify, render_template
from datetime import datetime, timezone
from zoneinfo import ZoneInfo
import requests

app = Flask(__name__)
@app.route("/")
def inicio():
    return render_template("pagina.html")

api_key = "bfb67620cb5407df38125216583bdf35"

@app.route("/clima")
def obtener_clima():

    ciudad = request.args.get("ciudad")

    url = f"https://api.openweathermap.org/data/2.5/weather?q={ciudad}&appid={api_key}&units=metric&lang=es"
    respuesta = requests.get(url)

    datos = respuesta.json()

    if respuesta.status_code != 200:
        return jsonify({
            "respuesta": "No se encontró la ciudad."
        })

    temperatura = datos["main"]["temp"]
    descripcion = datos["weather"][0]["description"]
    humedad = datos["main"]["humidity"]

    return jsonify({
        "respuesta": f"🌡️ Temperatura: {temperatura}°C | ☁️ Estado: {descripcion} | 💧 Humedad: {humedad}%"
    })

@app.route("/futbol")
def obtener_futbol():

    consulta = request.args.get("consulta")

    # Buscar el equipo
    url = f"https://www.thesportsdb.com/api/v1/json/123/searchteams.php?t={consulta}"

    respuesta = requests.get(url)
    datos = respuesta.json()

    if datos["teams"] is None:
        return jsonify({
            "respuesta": "❌ No encontré ese equipo."
        })

    equipo = datos["teams"][0]

    # Obtener el ID del equipo
    id_equipo = equipo["idTeam"]

    # Buscar el próximo partido
    url_partido = f"https://www.thesportsdb.com/api/v1/json/123/eventsnext.php?id={id_equipo}"

    respuesta_partido = requests.get(url_partido)
    datos_partido = respuesta_partido.json()

    if datos_partido["events"]:

        partido = datos_partido["events"][0]

        rival_local = partido.get("strHomeTeam", "No disponible")
        rival_visitante = partido.get("strAwayTeam", "No disponible")
        fecha = partido.get("dateEvent", "No disponible")
        hora = partido.get("strTime", "No disponible")
        estadio_partido = partido.get("strVenue", "No disponible")

    else:

        rival_local = "No disponible"
        rival_visitante = "No disponible"
        fecha = "No disponible"
        hora = "No disponible"
        estadio_partido = "No disponible"

    # Información del equipo
    nombre = equipo.get("strTeam", "No disponible")
    liga = equipo.get("strLeague", "No disponible")
    pais = equipo.get("strCountry", "No disponible")
    estadio = equipo.get("strStadium", "No disponible")
    fundacion = equipo.get("intFormedYear", "No disponible")
    genero = equipo.get("strGender", "No disponible")
    entrenador = equipo.get("strManager", "No disponible")
    descripcion = equipo.get("strDescriptionEN", "")

    if descripcion:
        descripcion = GoogleTranslator(
            source="auto",
            target="es"
        ).translate(descripcion)

    return jsonify({
        "respuesta":
        f"""
        ⚽ <b>{nombre}</b><br><br>

        🏆 Liga: {liga}<br>
        🌍 País: {pais}<br>
        🏟️ Estadio: {estadio}<br>
        📅 Fundación: {fundacion}<br>
        👥 Categoría: {genero}<br><br>

        📅 <b>Próximo partido:</b><br><br>

        🏠 {rival_local}<br>
        🆚 {rival_visitante}<br>
        📅 Fecha: {fecha}<br>
        🕒 Hora: {hora}<br>
        🏟️ Estadio: {estadio_partido}<br><br>

        📌 <b>Información:</b><br><br>

        {descripcion}
        """
    })


if __name__ == "__main__":
    app.run(debug=True)