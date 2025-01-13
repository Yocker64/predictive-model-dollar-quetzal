import requests
import pandas as pd
from xml.etree import ElementTree

# SOAP endpoint and headers
url = "https://banguat.gob.gt/variables/ws/TipoCambio.asmx"
options = {
    "Content-Type": "text/xml; charset=utf-8"
}

# SOAP request body
SOAPEnvelop = """<soap:Envelope xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns:xsd="http://www.w3.org/2001/XMLSchema" xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/">
  <soap:Body>
    <TipoCambioFechaInicial xmlns="http://www.banguat.gob.gt/variables/ws/">
      <fechainit>2025-01-01</fechainit>
    </TipoCambioFechaInicial>
  </soap:Body>
</soap:Envelope>"""

# Make the POST request
response = requests.post(url, data=SOAPEnvelop, headers=options)
# 


# Check if the request was successful
if response.status_code == 200:
    print("SOAP request successful!")
    # Print raw response (for debugging)
else:
    print(f"Error: {response.status_code}")


# Parse the XML response
root = ElementTree.fromstring(response.text)

# Define namespaces 
namespaces = {
    'soap': 'http://schemas.xmlsoap.org/soap/envelope/',
    'ns': 'http://www.banguat.gob.gt/variables/ws/'
}

# Find all <Var> elements in the response
data = []
for var in root.findall(".//ns:Var", namespaces):
    fecha = var.find("ns:fecha", namespaces).text
    venta = var.find("ns:venta", namespaces).text
    data.append({"Fecha": fecha, "Venta": float(venta)})



# for child in root.iter("{http://www.banguat.gob.gt/variables/ws/}TipoCambioFechaInicialResult"):
#     print(child.find("{http://www.banguat.gob.gt/variables/ws/}fecha").text)
    # date = child.find("ns:fecha", namespaces).text 
    # rate = child.find("ns:valor", namespaces).text
    # data.append({"Date": date,"Rate": rate})


# Find all `TipoCambio` entries (modify this based on actual tags)
# for entry in root.findall(".//ns:TipoCambio", namespaces):
#     date = entry.find("ns:fecha", namespaces).text 
#     rate = entry.find("ns:valor", namespaces).text
#     data.append({"Date": date, "Rate": rate})

# Convert to a pandas DataFrame
df = pd.DataFrame(data)

df['Fecha'] = pd.to_datetime(df['Fecha'], format='mixed')

# Convert 'Rate' column to float
df['Venta'] = pd.to_numeric(df['Venta'])

# Example: Filter data by date range
filtered_df = df[df['Fecha'] > '2025-01-01']

# Example: Calculate average rate
average_rate = df['Venta'].mean()
print(f"Average Rate: {average_rate}")