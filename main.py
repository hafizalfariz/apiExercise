
from fastapi import FastAPI, HTTPException, Header
import pandas as pd

app = FastAPI()

api_key = "adminrmt045"

@app.get("/")
def home():
  return "Selamat Datang di Toko Hacktiv 8"

# buat endpoint untuk baca dataToko
@app.get("/data")
def readData():
  df = pd.read_csv("dataToko.csv")
  return df.to_dict(orient='records')

#buat endpoint untuk baca dataToko berdasarkan endpoint baru
@app.get("/data/{user_input}")
def searchById(user_input: int):
  # baca data dulu
    df = pd.read_csv("dataToko.csv")
 
  # matching apakah user_input sesuai dengan data yang ada atau tidak
    filter = df[df["id"] == user_input]


  #buat kondisi jika tidak ada --> len ()
    if len(filter) == 0:
       raise HTTPException(status_code=404, detail="Barang tidak ada.")


  #jika ada maka ditampilkan melalui return
    return filter.to_dict(orient='records')



# buat endpoint untuk update data ke data yang sudah ada diserver
@app.post("/item/{item_id}")
def addData(item_id: int, item_name: str, item_price: float):
    # baca data yang sudah ada dulu
    df = pd.read_csv("dataToko.csv")
   
    # buat dict baru untuk tempat data baru
    new_data = {
       "id": item_id,
       "namaBarang" : item_name,
       "harga" : item_price
    }


    # ubah dict baru ke dataframe
    new_df = pd.DataFrame(new_data, index=[0])



    # kita gabungkan(concat) data baru dengan data yang sudah ada
    df = pd.concat([df,new_df], ignore_index=True)

    # save data yang sudah terupdate ke csv
    df.to_csv("dataToko.csv", index=False)

    return f"Data dengan id {item_id} nama barang {item_name} dan harga {item_price} sudah ditambahkan"

# Buat endpoint baru untuk update isi data yang sudah ada diserver

@app.put("/update/{item_id}")
def updateData(item_id: int, item_name: str, item_price: float):
    
    df = pd.read_csv("dataToko.csv")
   
    # buat dict baru untuk tempat data baru
    update_data = {
       "id": item_id,
       "namaBarang" : item_name,
       "harga" : item_price
    }
    # Cek jika id yang dimasukan tidak ditemukan

    if update_data["id"] not in df["id"].values:
       return "Data dengan id {item_id} tidak ditemukan."
    
    # replace/update data jika id ditemukan

    df.loc[df["id"] == update_data["id"], "namaBarang"] = update_data["namaBarang"]
    df.loc[df["id"]==update_data["id"], "harga"] = update_data["harga"]

    # simpan data terupdate ke csv

    df.to_csv("dataToko.csv", index=False)

    return "Barang dengan id {item_id} nama barang {item_name} sudah terupdate."





# Buat endpoint untuk memasukan data baru

@app.get("/income")
def readIncome(password:str=Header(None)):
   
   # verifikasi api key = password
   if password==None:
      raise HTTPException(status_code=401, detail="Password harus diisi.")
   elif password!=api_key:
      raise HTTPException(status_code=401, detail="Anda tidak mempunyai akses.")
   else:
   
   #  jika password diisi dan sesuasi api_key maka data dimunculkan
      
        df_income = pd.read_csv("dataIncome.csv")
        return df_income.to_dict(orient="records")





