import socket
import json
import uuid

def send_tm_request(request):

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect(('localhost', 6666))
    data = json.dumps(request)
    s.send(data.encode())
    s.close()

if __name__ == "__main__":

    request = {'Credential': uuid.uuid1().__str__(),
               'filePath': 'E:\Ethan_Github\Python_Fundamental\data\sample.xlsx',
               'exportType': ['excel', 'tmx']
               }
    # request = None
    send_tm_request(request)