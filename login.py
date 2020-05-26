from function import *

# client = Boteater(my_token='token_here',my_app="ios_ipad")
client = Boteater(my_app="ios_ipad")
clientMid = client.profile.mid


temporary = {
    "unsend": {}
}


def my_worker(op):
    if op.type in [25, 26]:
        msg = op.message
        text = str(msg.text)
        msg_id = msg.id
        receiver = msg.to
        msg.from_ = msg._from
        sender = msg._from
        cmd = text.lower()
        if msg.toType == 0 and sender != clientMid:
            to = sender
        else:
            to = receiver

        if cmd == "tagall":
            client.sendTagAll(to)

        if msg.contentType == 0:
            temporary["unsend"][msg.id] = {
                "text": msg.text, "type": "text", "from": msg._from}
            print(temporary["unsend"])

        if op.type == 65:
            if msg_id in temporary["unsend"]:
                if temporary["unsend"][msg_id]["type"] == "text":
                    client.sendMessage(to, temporary["unsend"][msg_id]["text"])
            print("[ OP ] Detectunsend")


def run():
    while True:
        try:
            ops = client.fetchOperation()  # For Secondary Token
            for op in ops:
                if op.revision > client.lastOP:
                    client.lastOP = max(op.revision, client.lastOP)
                    my_worker(op)
                    ## Don't threading in here :) ##
        except Exception as e:
            print(e)


if __name__ == "__main__":
    run()
