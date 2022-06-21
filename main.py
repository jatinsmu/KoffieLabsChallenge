from fastapi import FastAPI
from fastapi.responses import FileResponse
import uvicorn
import database
import requests
import json

# initialize the fast api
app = FastAPI()


@app.get("/")
async def root():
    """
    Default endpoint
    :return: Json dictionary having default message
    """
    return {"message": "Welcome to the default endpoint"}


@app.get("/lookup")
async def lookup(vin):
    """
    Lookup the detail of Vin. If details are present in cache db, return from there. Else get details from the external Api.
    :param vin: Alphanumeric string of length 17
    :return: Decoded Vin details in Json dictionary format
    """
    if is_vin_valid(vin):
        try:
            vin = str(vin)
            # create a connection to the database
            connection = database.create_connection(db)
            result = database.get_data(connection, vin)

            if result:
                cached_result = True
                make = result[0][1]
                model = result[0][2]
                model_year = result[0][3]
                body_class = result[0][4]
            else:
                cached_result = False
                make, model, model_year, body_class = get_details_from_api(vin)

            if make:
                # if make is not None
                json_result = {'Input VIN Requested': vin,
                               'Make': make,
                               'Model': model,
                               'Model Year': model_year,
                               'Body Class': body_class,
                               'Cached Result': cached_result
                               }
            else:
                json_result = {'message': 'Error in getting data for the request VIN'}
            return json_result
        except:
            return {'message': 'Error in getting data for the request VIN'}
    else:
        return {'message': 'VIN is not in a valid format of 17 alphanumeric characters'}


@app.get("/remove")
async def remove(vin):
    """
    Remove the details for a specific vin from the database
    :param vin: Alphanumeric string of length 17
    :return: Json dictionary containing vin and boolean success message
    """
    try:
        vin = str(vin)
        # Check if record exists
        connection = database.create_connection(db)
        result = database.get_data(connection, vin)
        if result:
            # delete
            connection = database.create_connection(db)
            removal = database.delete_data(connection, vin)
        else:
            removal = False

        return {"Input VIN Requested": vin,
                "Cache Delete Success": removal
                }
    except:
        return {'message': 'Error in deleting VIN from the database'}


@app.get("/export")
async def export():
    """
    Export database and send to the client
    :return: Database parquet file
    """
    try:
        connection = database.create_connection(db)
        exported = database.export_db(connection)
        if exported:
            file_path = 'export.parquet'
            return FileResponse(file_path)
        else:
            return {'message': 'Error in exporting the database cache'}

    except:
        return {'message': 'Error in exporting the database cache'}


def get_details_from_api(vin):
    """
    Function to query the external API for the Vin details
    :param vin: Alphanumeric string of length 17
    :return: make, model, model_year, body_class for that particular Vin
    """
    try:
        url = "https://vpic.nhtsa.dot.gov/api/vehicles/DecodeVinValues/{}?format=json".format(vin)
        result = requests.get(url)
        if result.status_code == 200:
            response = json.loads(result.text).get('Results')[0]
            make = response.get('Make', '')
            model = response.get('Model', '')
            model_year = response.get('ModelYear', '')
            body_class = response.get('BodyClass', '')

            # store results in database
            data = {'VIN': vin,
                    'Make': make,
                    'Model': model,
                    'Model Year': model_year,
                    'Body Class': body_class
                    }
            connection = database.create_connection(db)
            database.create_table(connection)
            connection = database.create_connection(db)
            database.insert_data(connection, data)

            return make, model, model_year, body_class
    except Exception as error:
        print("Failed to get response from API: ", error)
        return None, None, None, None


def is_vin_valid(vin):
    """
    Function to check if input vin is valid or not
    :param vin: Vin sent to the server from Client
    :return: Boolean True or False
    """
    vin = str(vin)
    # Check if length is 17 and vin is alphanumeric
    if len(vin) != 17 or not vin.isalnum():
        return False
    else:
        return True


if __name__ == "__main__":
    db = 'cache.db'
    uvicorn.run(app, host="0.0.0.0", port=8000)
