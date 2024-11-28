import random
import os
import ptbot
from dotenv import load_dotenv
from pytimeparse import parse


def render_progressbar(total, iteration, prefix='', suffix='', length=30, fill='█', zfill='░'):
    iteration = min(total, iteration)
    percent = "{0:.1f}"
    percent = percent.format(100 * (iteration / float(total)))
    filled_length = int(length * iteration // total)
    pbar = fill * filled_length + zfill * (length - filled_length)
    return '{0} |{1}| {2}% {3}'.format(prefix, pbar, percent, suffix)

def choose(author_id, bot_choose):
    answer = 'Время вышло'
    bot_choose.send_message(author_id, answer)

def notify_progress(secs_left, author_id, message_id, question, bot_notify):
    answer = "Осталось секунд {0}\n{1}".format(secs_left, render_progressbar(parse(question), secs_left))
    bot_notify.update_message(author_id, message_id, answer)

def wait(chat_id, question, bot_wait):
    message_id = bot_wait.send_message(chat_id, "Таймер запущен")
    bot_wait.create_timer(parse(question), choose, author_id=chat_id, bot_choose=bot_wait)
    bot_wait.create_countdown(parse(question), notify_progress, author_id=chat_id, message_id=message_id, question=question, bot_notify=bot_wait)

def main():

    load_dotenv()

    bot = ptbot.Bot(os.environ['TG_TOKEN'])

    bot.reply_on_message(wait, bot_wait=bot)

    bot.run_bot()

if __name__ == '__main__':
    main()