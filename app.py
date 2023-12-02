from flask import Flask, request, render_template_string
import socket
import json

app = Flask(__name__)

# HTML Template z Bootstrapem dla strony głównej i odpowiedzi
HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title>Wake on LAN</title>
    <!-- Dodanie Bootstrap CSS -->
    <link rel="stylesheet" href="https://stackpath.bootstrapcdn.com/bootstrap/4.5.2/css/bootstrap.min.css">
    <link rel="shortcut icon" type="image/x-icon" href="{{ url_for('static', filename='favicon.png') }}">
     <style>
        #identifier {
            width: 100px;  /* Ustawienie szerokości pola tekstowego */
        }
        .btn-primary {
            width: 100px; /* Ustawienie szerokości przycisku */
        }
    </style>
</head>
<body>
    <div class="container">
        <img src="{{ url_for('static', filename='primes.jpg') }}" alt="Logo" style="width: 500px;">
        <h1 class="mt-5">Usługa uruchomienia komputera</h1> 
        <form action="/" method="post" class="mt-4">
            <div class="form-group">
                <label for="identifier">Numer stacji:</label>
                <input type="text" class="form-control" id="identifier" name="identifier" required>
            </div>
            <button type="submit" class="btn btn-primary">Uruchom</button>
        </form>
        {% if message %}
            <p class="mt-3 {{ 'text-success' if color == 'green' else 'text-danger' }}">{{ message }}</p>
        {% endif %}
    </div>
    <!-- Opcjonalnie, dodanie Bootstrap JS i zależności -->
    <script src="https://code.jquery.com/jquery-3.5.1.slim.min.js"></script>
    <script src="https://cdn.jsdelivr.net/npm/@popperjs/core@2.0.5/dist/umd/popper.min.js"></script>
    <script src="https://stackpath.bootstrapcdn.com/bootstrap/4.5.2/js/bootstrap.min.js"></script>
</body>
</html>
"""

def send_wol_packet(mac_address):
    mac_bytes = bytes.fromhex(mac_address.replace(':', ''))
    magic_packet = b'\xff' * 6 + mac_bytes * 16
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as sock:
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
        sock.sendto(magic_packet, ('<broadcast>', 9))
    return True

@app.route('/', methods=['GET', 'POST'])
def index():
    with open('mac_addresses.json', 'r') as file:
        mac_map = json.load(file)

    message = None
    color = "black"

    if request.method == 'POST':
        identifier = request.form['identifier'].lower()
        mac_address = next((mac for id, mac in mac_map.items() if id.lower() == identifier), None)

        if mac_address:
            send_wol_packet(mac_address)
            message = "Wysłano żądanie włączenia komputera."
            color = "green"
        else:
            message = f"Nie znaleziono komputera o numerze {identifier}."
            color = "red"

    return render_template_string(HTML_TEMPLATE, message=message, color=color)

if __name__ == '__main__':
    app.run(debug=True)
