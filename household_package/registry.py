import time
import pickle
from household_package.params import *
from google.cloud import storage


def save_model(model,type='baseline'):
    """
    Persist trained model locally on the hard drive at f"{LOCAL_REGISTRY_PATH}/models/{timestamp}.h5"
    - if MODEL_TARGET='gcs', also persist it in your bucket on GCS at "models/{timestamp}.h5" --> unit 02 only
    - if MODEL_TARGET='mlflow', also persist it on MLflow instead of GCS (for unit 0703 only) --> unit 03 only
    """
    try:
        timestamp = time.strftime("%Y%m%d-%H%M%S")
        file_path = f"../01-household-energy/model_h5/{type}/{type}_{timestamp}.pkl"
        with open(file_path, 'wb') as file:
            pickle.dump(model, file)

        print("Locally saved .......... !!!")
        client = storage.Client()
        bucket = client.bucket(BUCKET_NAME)
        blob = bucket.blob(f"models/{type}_{timestamp}.pkl")
        blob.upload_from_filename(file_path)
        print("GCS saved .......... !!!")


        return None
    except:
        raise "You have a fatal error, pay 50 euros"

    # client = storage.Client()
    #     bucket = client.bucket(BUCKET_NAME)
    #     blob = bucket.blob(f"models/{model_filename}")
    #     blob.upload_from_filename(model_path)

        # print("✅ Model saved to GCS")

        # return None
