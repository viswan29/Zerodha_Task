import datetime
import requests
import zipfile
import io,os
import csv
import redis

def get_download_path():
    scraper_folder = os.path.join(os.getcwd(), "csv_files")
    return scraper_folder

def read_local(file_path):
    records = csv.DictReader(open(file_path))
    return list(records)

def redis_connection():
    redis_host = '0.0.0.0'
    redis_port = int(os.environ.get('PORT'))
    redis_password = None
    r = redis.StrictRedis(host=redis_host, port=redis_port, password=redis_password, decode_responses=True)
    return r 

def Bhavcopy_bse_downloader(date):
    date_string = date.strftime("%d%m%y")
    
    url = "https://www.bseindia.com/download/BhavCopy/Equity/EQ" + date_string + "_CSV.ZIP"
    
    response = requests.request("GET",url)
    if response.status_code ==200:
        z = zipfile.ZipFile(io.BytesIO(response.content))
        z.extractall(path=get_download_path())
    
    downloaded_filename = "EQ" + date_string + ".CSV"

    try:
        download_file_path = os.path.join(get_download_path(), downloaded_filename)
        records = read_local(file_path=download_file_path)
    except FileNotFoundError:
        print("FILE NOT FOUND")
        return []
    return records

if __name__ == "__main__":

    records = Bhavcopy_bse_downloader(
        date=datetime.datetime.utcnow().date() - datetime.timedelta(days=4)
    )
    r = redis_connection()
    for record in records:
        r.hmset(record["SC_NAME"], record)

    