import logging
import random
import re
from datetime import datetime,date

logger = logging.getLogger(__name__)


class Messenger(object):
    def __init__(self, slack_clients):
        self.clients = slack_clients

    def send_message(self, channel_id, msg):
        # in the case of Group and Private channels, RTM channel payload is a complex dictionary
        if isinstance(channel_id, dict):
            channel_id = channel_id['id']
        logger.debug('Sending msg: {} to channel: {}'.format(msg, channel_id))
        channel = self.clients.rtm.server.channels.find(channel_id)
        channel.send_message("{}".format(msg.encode('ascii', 'ignore')))

    def write_help_message(self, channel_id):
        bot_uid = self.clients.bot_user_id()
        txt = '{}\n{}\n{}\n{}\n{}'.format(
            "I'm your friendly Slack bot written in Python.  I'll *_respond_* to the following commands:",
            "> `hi <@" + bot_uid + ">` - I'll respond with a randomized greeting mentioning your user. :wave:",
            "> `<@" + bot_uid + "> joke` - I'll tell you one of my finest jokes, with a typing pause for effect. :laughing:",
            "> `<@" + bot_uid + "> attachment` - I'll demo a post with an attachment using the Web API. :paperclip:",
            "> `<@" + bot_uid + "> countdown yyyy-mm-dd` - I'll give you a day countdown to that date...iso format obvs :uk:")
        self.send_message(channel_id, txt)

    def write_greeting(self, channel_id, user_id):
        greetings = ['Hi', 'Hello', 'Nice to meet you', 'Howdy', 'Salutations']
        txt = '{}, <@{}>!'.format(random.choice(greetings), user_id)
        self.send_message(channel_id, txt)

    def write_prompt(self, channel_id):
        bot_uid = self.clients.bot_user_id()
        txt = "I'm sorry, I didn't quite understand... Can I help you? (e.g. `<@" + bot_uid + "> help`)"
        self.send_message(channel_id, txt)

    def write_joke(self, channel_id):
        question = "Why did the python cross the road?"
        self.send_message(channel_id, question)
        self.clients.send_user_typing_pause(channel_id)
        answer = "To eat the chicken on the other side! :laughing:"
        self.send_message(channel_id, answer)


    def write_error(self, channel_id, err_msg):
        txt = ":face_with_head_bandage: my maker didn't handle this error very well:\n>```{}```".format(err_msg)
        self.send_message(channel_id, txt)

    def demo_attachment(self, channel_id):
        txt = "Beep Beep Boop is a ridiculously simple hosting platform for your Slackbots."
        attachment = {
            "pretext": "We bring bots to life. :sunglasses: :thumbsup:",
            "title": "Host, deploy and share your bot in seconds.",
            "title_link": "https://beepboophq.com/",
            "text": txt,
            "fallback": txt,
            "image_url": "https://storage.googleapis.com/beepboophq/_assets/bot-1.22f6fb.png",
            "color": "#7CD197",
        }
        self.clients.web.chat.post_message(channel_id, txt, attachments=[attachment], as_user='true')

    def day_countdown(self, channel_id, input_text):
        rgx = re.search("\d{4}[-]\d{2}[-]\d{2}",input_text)
        if rgx:
            date_str = rgx.group()
            from_date = date.today()
            to_date = datetime.strptime(date_str,'%Y-%m-%d').date()
            days = abs((to_date-from_date).days)
            if days > 1:
                mod = 'days'
            else:
                mod = 'day'
            txt = ":clock1: only *"+str(days)+mod+"* until "+date_str+"!!! :thumbsup: :sparkles: :boom: :tada:"
        else:
            txt = "Sure you gave me that date in the correct format? `yyyy-mm-dd`"
        self.send_message(channel_id, txt)

    def yoda(self, channel_id):
        txt = ":point_up: do or do not, there is no try."
        self.send_message(channel_id, txt)

    def king_julian(self, channel_id):
        txt = "If I King Julian (that's my name) only had two days to live, I would do all the things I have ever dreamed of doing. I would love to become a professional whistler. I'm pretty amazing at it now, but I wanna get, like, even better. :kissing: :dash: :sweat_drops: :umbrella_with_rain_drops: And you know what else I would do? I would invade a neighboring country and impose my own ideology on them, even if they didn't want it!."
        self.send_message(channel_id, txt)
