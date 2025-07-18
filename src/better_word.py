import logging

from slack_bolt import App
from slack_bolt.adapter.socket_mode import SocketModeHandler

from src.config import config
from src.manager import BetterWordManager

logging.basicConfig(level=logging.DEBUG)


app = App(token=config["SLACK_BOT_TOKEN"])


@app.command("/better")
def better_command(ack, respond, body):
    ack("请稍等，正在生成更好的词语...")
    better_word = BetterWordManager.get_better_word(body["text"])
    print(f"Better word: {better_word}")
    respond(f"❌{body["text"]}\n----\n✅{better_word}")


def main():
    SocketModeHandler(app, config["SLACK_APP_TOKEN"]).start()


if __name__ == "__main__":
    main()
