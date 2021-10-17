import os
import sys
import re
from pprint import pprint

import inquirer
from inquirer import errors

sys.path.append(os.path.realpath('.'))


def nub_validation(answers, current):
    if not re.match('[0-9]{10}', current):
        raise errors.ValidationError('', reason='请输入正确的10位学号')

    return True




questions = [
    inquirer.Text('name',
                  message="What's your name?"),
    inquirer.Text('surname',
                  message="What's your surname, {name}?"),
    inquirer.Text('phone',
                  message="What's your phone number",
                  validate=nub_validation
                  )
]

answers = inquirer.prompt(questions)

pprint(answers)