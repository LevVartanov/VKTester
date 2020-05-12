from enum import Enum
import vk_api
from vk_api.bot_longpoll import VkBotLongPoll, VkBotEventType
import random
from vk_api.keyboard import VkKeyboard
from Back import query_tests, Inquirer, Exam

APP_TOKEN = '5aa21cc5de80c1816b50166182bf710fc945d6f9e7b6a607f49c8d8bf9dedc77eb428dff9e98b830b29d6'
GROUP_ID = '194431619'
HELLO = 'Привет! Я - бот VKTester. Я совместим с приложением PyTester. ' \
        'Используйте его, чтобы создавать новые тесты. Ниже приведён список ' \
        'тестов, которые у меня есть. Чтобы выбрать тест или ответ, нажмите ' \
        'на соответствующую кнопку или введите его номер. Чтобы прервать ' \
        'прохождение теста и вернуться к начальному меню, введите "начать".'
SORRY = 'Извините, я не могу понять Вас. Поажлуйста, повторите ответ, ' \
        'соблюдая инструкцию.'
vk_session = vk_api.VkApi(token=APP_TOKEN)
vk = vk_session.get_api()


class TestState(Enum):
    idle = 1
    choosing_test = 2
    testing = 3


class Message:
    def __init__(self, question, answers, user_id):
        message = question
        answers_keyboard = VkKeyboard(one_time=True)
        first = True
        number = 1
        for i in answers:
            message = message + '\n' + str(number) + '. ' + i
            if not first:
                answers_keyboard.add_line()
            answers_keyboard.add_button(i, payload=str(number))
            first = False
            number += 1
        answers_keyboard_json = answers_keyboard.get_keyboard()
        vk.messages.send(user_id=user_id,
                         message=message,
                         random_id=random.randint(0, 2 ** 64),
                         keyboard=answers_keyboard_json)


def check(answer, answers):
    if 'payload' in answer:
        index = int(answer['payload'])
    elif answer['text'].isdigit() and int(answer['text']) <= len(answers):
        index = int(answer['text'])
    else:
        return -1
    return index - 1

def choosing_test(message, tests, tests_names):
    index = check(message, tests_names)
    current_test = None
    if index != -1:
        test = tests[index]
        if test.type == 'опросник':
            current_test = Inquirer(test)
        else:
            current_test = Exam(test)

        #question, answers = current_test.question(0)
        #answers_text = [answer.answer for answer in answers]
        #question_message = Message(question, answers_text, message['from_id'])
    #else:
        #repeat_tests_message = Message(SORRY, tests_names, message['from_id'])
    return current_test


def answer_question(message, test, question_number):
    question, answers = test.question(question_number)
    answers_text = [answer.answer for answer in answers]
    Message(question, answers_text, message['from_id'])
    return answers, answers_text


def main():
    tests = query_tests()
    tests_names = [string.test for string in tests]

    test_state = TestState.idle
    longpoll = VkBotLongPoll(vk_session, GROUP_ID)

    question_number = 0
    user_answers = []

    for event in longpoll.listen():
        if event.type == VkBotEventType.MESSAGE_NEW:
            if event.obj.message['text'].lower() == 'начать':
                Message(HELLO, tests_names, event.obj.message['from_id'])
                test_state = TestState.choosing_test
            elif test_state == TestState.choosing_test:
                current_test = choosing_test(event.obj.message, tests,
                                            tests_names)
                if current_test:
                    test_state = TestState.testing

                    user_answers = []
                    answers, answers_text = answer_question(
                        event.obj.message, current_test, 0)
                    question_number = 1
                else:
                     Message(SORRY, tests_names, event.obj.message['from_id'])
            elif test_state == TestState.testing:
                index = check(event.obj.message, answers_text)
                if index != -1:
                    user_answers.append(answers[index].marker)
                    if question_number < current_test.questions_count:
                        answers, answers_text = answer_question(
                            event.obj.message, current_test, question_number)
                        question_number += 1
                    else:

                        vk.messages.send(user_id=event.obj.message['from_id'],
                                         message=current_test.result(
                                             user_answers),
                                         random_id=random.randint(0, 2 ** 64))
                else:
                    Message(SORRY, answers_text, event.obj.message['from_id'])


if __name__ == '__main__':
    main()
