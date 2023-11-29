import time
import pickle
from household_package.params import *
from google.cloud import storage
#from tensorflow import keras


def save_model(model,type='baseline'):
    """
    Persist trained model locally on the hard drive at f"{LOCAL_REGISTRY_PATH}/models/{timestamp}.h5"
    - if MODEL_TARGET='gcs', also persist it in your bucket on GCS at "models/{timestamp}.h5" --> unit 02 only
    - if MODEL_TARGET='mlflow', also persist it on MLflow instead of GCS (for unit 0703 only) --> unit 03 only
    """
    timestamp = time.strftime("%Y%m%d-%H%M%S")
    file_path = f"../01-household-energy/model_h5/{type}/{type}_{timestamp}.pkl"
    with open(file_path, 'wb') as file:
        pickle.dump(model, file)
    print("Locally saved .......... !!!")

    try:
        client = storage.Client()
        bucket = client.bucket(BUCKET_NAME)
        blob = bucket.blob(f"models/{type}_{timestamp}.pkl")
        blob.upload_from_filename(file_path)
        print("GCS saved .......... !!!")
        #https://storage.cloud.google.com/01_household_energy/models/baseline_20231129-122043.pkl

        return None
    except:
        raise "You have a fatal error, pay 50 euros"

    # client = storage.Client()
    #     bucket = client.bucket(BUCKET_NAME)
    #     blob = bucket.blob(f"models/{model_filename}")
    #     blob.upload_from_filename(model_path)

        # print("✅ Model saved to GCS")

        # return None

def load_model(model_type='baseline'): #-> keras.Model: #stage="Production"
    """
    Return a saved model:
    - locally (latest one in alphabetical order)
    - or from GCS (most recent one) if MODEL_TARGET=='gcs'  --> for unit 02 only
    - or from MLFLOW (by "stage") if MODEL_TARGET=='mlflow' --> for unit 03 only

    Return None (but do not Raise) if no model is found

    """

    #MODEL_TARGET == "gcs":
    # 🎁 We give you this piece of code as a gift. Please read it carefully! Add a breakpoint if needed!
    #print(Fore.BLUE + f"\nLoad latest model from GCS..." + Style.RESET_ALL)
    client = storage.Client()
    blobs = list(client.get_bucket(BUCKET_NAME).list_blobs(prefix="model"))
    try:
        latest_blob = max(blobs, key=lambda x: x.updated)
        latest_model_path_to_save = os.path.join(LOCAL_REGISTRY_PATH, latest_blob.name)
        latest_blob.download_to_filename(latest_model_path_to_save)

        # for sklearn (baseline)
        if model_type=='baseline':
            with open(latest_model_path_to_save , 'rb') as f:
                latest_model = pickle.load(f)
        #else:
            # for tf.keras models
            #latest_model = keras.models.load_model(latest_model_path_to_save)
        print("✅ Latest model downloaded from cloud storage")
        return latest_model

    except:
        print(f"\n❌ No model found in GCS bucket {BUCKET_NAME}")
        return None
