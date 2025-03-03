import paho.mqtt.client as mqtt

MQTT_BROKER = "172.20.10.2"
MQTT_PORT = 1883
MQTT_TOPIC = "camera/image"

i = 0
buffer = bytearray()  # 用于存储完整图片数据
receiving = False      # 标志是否正在接收图片数据

def on_message(client, userdata, msg):
    global i, buffer, receiving

    payload = msg.payload.decode(errors="ignore")  # 尝试解码

    if payload == "START":
        print("📸 接收到图片起始信号")
        buffer = bytearray()
        receiving = True
        return
    elif payload == "END":
        print(f"📸 接收到图片结束信号，图片大小: {len(buffer)} bytes")
        outPutPath = f"../received/received_{i}.jpeg"
        i += 1
        with open(outPutPath, "wb") as f:
            f.write(buffer)
        print(f"✅ 图片保存成功: {outPutPath}")
        buffer = bytearray()  # 清空缓冲区
        receiving = False
        return

    if receiving:
        buffer.extend(msg.payload)  # 追加数据

client = mqtt.Client()
client.on_message = on_message

client.connect(MQTT_BROKER, MQTT_PORT, 60)
client.subscribe(MQTT_TOPIC)

print(f"📡 监听 MQTT 主题: {MQTT_TOPIC}，等待图片数据...")
client.loop_forever()
