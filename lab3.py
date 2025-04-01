# importing pubnub libraries
from pubnub.pubnub import PubNub, SubscribeListener, SubscribeCallback,PNStatusCategory
from pubnub.pnconfiguration import PNConfiguration
from pubnub.exceptions import PubNubException
import pubnub
import RPi.GPIO as GPIO
from mfrc522 import SimpleMFRC522
pnconf = PNConfiguration()
# create pubnub_configuration_object
pnconf.publish_key = 'pub-c-85ba3694-4855-4861-a14b-fdfcb90cf839' # set pubnub publish_key
pnconf.subscribe_key = 'sub-c-7c1de1d9-ea5b-451f-bb88-35ae502a81c4' # set pubnub subscibe_key
pnconf.uuid = 'userId'
pubnub = PubNub(pnconf)
# create pubnub_object using pubnub_configuration_object
channel='chenweisong728'
# provide pubnub channel_name
data = {
'message': 'hi'
}
# data to be published
my_listener = SubscribeListener()
# create listner_object to read the msg from the Broker/Server
pubnub.add_listener(my_listener)
# add listner_object to pubnub_object to subscribe it
pubnub.subscribe().channels(channel).execute()
# subscribe the channel
my_listener.wait_for_connect()
# wait for the listener_obj to connect
print('connected')
# print confirmation msg
pubnub.publish().channel(channel).message(data).sync()
# publish the data to the mentioned channel
while True:
    result = my_listener.wait_for_message_on(channel)
    # Read the new msg on the channel
    print(result.message)
    print(result.message.keys())
    try:
        text = result.message
        print("Now place your tag to write")
        reader = SimpleMFRC522()
        reader.write(str(text))
        print("Written")
    finally:
        print("ok")
    try:
        id, text = reader.read()
        print("id",id)
        print("text", text)
#         pubnub.publish().channel(channel).message(data).sync()
    finally:
        GPIO.cleanup()
