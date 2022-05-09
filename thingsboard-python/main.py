import time,random,sys
from tb_device_mqtt import TBDeviceMqttClient

telemetry = {'temperature': 230}

def on_server_side_rpc_request(client, request_id, request_body):
    print(request_id, request_body,telemetry)
    if request_body["method"] == "getTurn":
        turn = 0 if "turn" not in telemetry else telemetry['turn'] 
        client.send_rpc_reply(request_id, turn)
        telemetry.update({"turn": turn})
    elif request_body["method"] == "setTurn":
        turn = request_body["params"]
        client.send_rpc_reply(request_id, turn)
        telemetry.update({"turn": 1 if turn else 0})
    print('response telemetry: ', telemetry)
    client.send_telemetry(telemetry)

def mock_telemetry():
    t = {
        "battery":random.choice(range(10,50)),
    }
    return t

def run(token):
    client = TBDeviceMqttClient("localhost", token)
    client.set_server_side_rpc_request_handler(on_server_side_rpc_request)
    client.connect()
    while True:
        time.sleep(3)
        tc = mock_telemetry()
        client.send_telemetry(tc)

if __name__ == '__main__':
    # idx = sys.argv[1]
    token = "NnnNpPtA2LSwDiHGqPTZ"
    run(token)