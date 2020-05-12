from Models import Test, Question, Answer, ResultInquirer, ResultExam, Criterion
from DBConnection import init_connection, create_session

INQUIRER_RESULT = 'Ваш результат:'
EXAM_RESULT = 'Ваши оценка и балл:'
system_db_name = "Система.db"

def query_tests():
    factory = init_connection(system_db_name)
    session = create_session(factory)
    tests_list = session.query(Test).all()
    session.close()
    return tests_list

class UniversalTest:
    def __init__(self, test):
        factory = init_connection(test.file_name)
        self.session = create_session(factory)
        self.questions_count = int(test.length)

    def question(self, index):
        question = self.session.query(Question)[index]
        return question.question, self.session.query(Answer).filter(
            Answer.question == question.id)


class Inquirer(UniversalTest):
    def result(self, user_answers):
        results = self.session.query(ResultInquirer).all()
        results_text = [result.result for result in results]
        differences = list()
        for res in results:
            current_result = res.answers.split()
            difference = 0
            for j in range(len(user_answers)):
                difference += (int(user_answers[j]) -
                               int(current_result[j])) ** 2
            differences.append(difference)
        results_differences = list()
        for i in range(len(results_text)):
            a = list()
            a.append(results_text[i])
            a.append(differences[i])
            results_differences.append(a)
        results_differences.sort(key=lambda z: z[1])
        result_max = results_differences[-1][1]
        dif_of_dif = result_max - results_differences[0][1]
        results_percents = list(map(lambda x: str(100 * (result_max - x[1]) /
                                                 dif_of_dif),
                                   results_differences))
        result_message = INQUIRER_RESULT
        for i in range(len(results_percents)):
            result_message += '\n' + results_differences[i][0] + ' - ' + \
                              str(results_percents[1]) + '%'
        return result_message


class Exam(UniversalTest):
    def result(self, user_answers):
        result = self.session.query(ResultExam)[0].answers.split()
        rating = 0
        for i in range(len(user_answers)):
            if user_answers[i] == int(result[i]):
                rating += 1
        mark = 1
        criterions_list = self.session.query(Criterion).all()

        for criterion in criterions_list:
            if rating >= criterion.criterion:
                mark = criterion.mark
                break
        result_message = EXAM_RESULT + '\n' + str(mark) + ' - ' + str(rating)
        return result_message
