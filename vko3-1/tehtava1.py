#the script should get JSON data from  https://2ri98gd9i4.execute-api.us-east-1.amazonaws.com/dev/academy-checkpoint2-json
#read the values of parameter fields and write them into a file called checkpoint.txt on separate lines (the file should be in the same dir)
#creates a new Cloud Storage bucket and saves checkpoint.txt there
#(push the codes into a public GitHub repository when finished)

#make sure the GOOGLE_APPLICATION_CREDENTIALS env. variable is set before running the script
#for details, check e.g. URLHERE

import requests 
from google.cloud import storage

def parameter_file(url='https://2ri98gd9i4.execute-api.us-east-1.amazonaws.com/dev/academy-checkpoint2-json'):
    #gets the parameters from the url given as the parameter (ha!), the one specified in the assigment is given as default
    print("Fetching the parameters...")
    parameter_list = []
    source = requests.get(url)
    data = source.json()
    for d in data['items']:
        parameter_list.append(d['parameter'])
    print("Done!")

    #writes (adds/assigns) the parameters into the file specified in the assignment
    print("Writing the parameters into the file 'checkpoint.txt'...\n...")
    with open('checkpoint.txt', 'a') as f:
        for param in parameter_list:
            f.write(param + "\n")
    print("All done!\nThe parameters are now written into the file.")


def transfer_file_to_a_new_bucket(bucketname: str, storageclass='STANDARD', location='us'):
    try: 
        #creates the file using the function scripted above
        parameter_file()
        #creates a new bucket, the name of which is given as the parameter (a default storage class and location are set but can be specified by the user)
        print("Creating the bucket...")
        storage_client = storage.Client()
        bucket = storage_client.bucket(bucketname)
        bucket.storage_class = storageclass
        new_bucket = storage_client.create_bucket(bucket, location=location)

        print(f"Created bucket {new_bucket.name} in {new_bucket.location} with storage class {new_bucket.storage_class}.")
        print(f"Uploading the .txt file into {new_bucket.name}...")

        bucket = storage_client.bucket(new_bucket.name)
        blob = bucket.blob('checkpoint.txt')
        blob.upload_from_filename('./checkpoint.txt')

        print(f"File uploaded to the new bucket.")
    
    except:
        raise OSError("Something went wrong.\nPlease try again.")
        
    