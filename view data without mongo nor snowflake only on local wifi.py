import requests
import json, time



startTime = time.time()

# Phone IP
PhoneIP = "192.168.1.232"



def grabData(IP):
    # Simple lil request grab
        response = requests.get(
        "http://"+PhoneIP+"/get",
        params={"Force1": "full", "Force2" : "full", "GyroX": "full", "GyroY": "full", "GyroZ": "full", 
                "AccelX": "full",
                "AccelY": "full", "AccelZ": "full"
                },
        timeout=5
        )
    
        response.raise_for_status()
    
    
        BoF = response.json()["buffer"]["Force1"]["buffer"][-1]
        Heel = response.json()["buffer"]["Force2"]["buffer"][-1]
        gyrox = response.json()["buffer"]["GyroX"]["buffer"][-1]
        gyroy = response.json()["buffer"]["GyroY"]["buffer"][-1]
        gyroz = response.json()["buffer"]["GyroZ"]["buffer"][-1]
        accelx = response.json()["buffer"]["AccelX"]["buffer"][-1]
        accely = response.json()["buffer"]["AccelY"]["buffer"][-1]
        accelz = response.json()["buffer"]["AccelZ"]["buffer"][-1]
        return [BoF, Heel, gyrox,gyroy,gyroz, accelx, accely, accelz]



# while True:
#     time.sleep(0.05)
#     allData = grabData(PhoneIP)
#     dataNames = ["BoF","Heel","gyrox","gyroy","gyroz","accelx","accely", "accelz"]

    # print("X: "+str(a/llData[2])+"___ Y:"+str(allData[3])+"_____ Z:"+str(allData[4])+"")
    # +Y = Left
    # -Y = Right
    
    # for i in range(len(allData)):
        # print(dataNames[i]+": "+str(allData[i]))




def grabALLData(IP):
    # Simple lil request grab
        response = requests.get(
        "http://"+PhoneIP+"/get",
        params={"Force1": "full", "Force2" : "full", "GyroX": "full", "GyroY": "full", "GyroZ": "full", 
                "AccelX": "full",
                "AccelY": "full", "AccelZ": "full"
                },
        timeout=5
        )
    
        response.raise_for_status()
    
    
        BoF = response.json()["buffer"]["Force1"]["buffer"]
        Heel = response.json()["buffer"]["Force2"]["buffer"]
        gyrox = response.json()["buffer"]["GyroX"]["buffer"]
        gyroy = response.json()["buffer"]["GyroY"]["buffer"]
        gyroz = response.json()["buffer"]["GyroZ"]["buffer"]
        accelx = response.json()["buffer"]["AccelX"]["buffer"]
        accely = response.json()["buffer"]["AccelY"]["buffer"]
        accelz = response.json()["buffer"]["AccelZ"]["buffer"]
        return [(time.time() - startTime),BoF, Heel, gyrox,gyroy,gyroz, accelx, accely, accelz]
