from collections import deque
import io
import itertools
import re
import token
import tokenize

PRECEDENCE = {'+' : 0,
              '|' : 0,
              '*' : 1,
              '&' : 1,
              '~' : 2,
              '!' : 3}

def shunting_yard(token_list):
    output = []
    operators = deque()
    for tok in token_list:
        if tok.type in [token.ENCODING, token.NEWLINE, token.ENDMARKER]:
            pass
        elif tok.type == token.NAME or tok.type == token.NUMBER:
            output.append(tok)
        elif tok.type == token.OP:
            if tok.string == '(':
                operators.append(tok)
            elif tok.string == ')':
                while operators[-1].string != '(':
                    output.append(operators.pop())
                operators.pop()  # discard '('
                # pop rest of operator stack to output
                operators.reverse()
                output += operators
                operators.clear()
            elif tok.string in ['+', '*', '~', '&', '|', '!']:
                while (operators and operators[-1].string != '('
                    and (PRECEDENCE[operators[-1].string] >= PRECEDENCE[tok.string])):

                    output.append(operators.pop())
                operators.append(tok)
            else:
                raise RuntimeError("Unknown operator" + str(tok))

    operators.reverse()
    output += operators

    return output


def pretty_rpn(rpn_tokens):
    return ' '.join((x.string for x in rpn_tokens))


def compute(rpn, variables):
    """Compute the truth value of an expression, based on the values of variables"""
    eval_stack = deque()

    for tok in rpn:
        if tok.type == token.NAME:
            eval_stack.append(variables[tok.string])
        elif tok.type == token.OP:
            if tok.string in ['*', '&']:
                # need to pop first because of python's short circuit evaluation
                a = eval_stack.pop()
                b = eval_stack.pop()
                eval_stack.append(a and b)

            elif tok.string in ['+', '|']:
                # need to pop first because of python's short circuit evaluation
                a = eval_stack.pop()
                b = eval_stack.pop()
                eval_stack.append(a or b)

            elif tok.string in ['~', '!']:
                eval_stack.append(not eval_stack.pop())
            else:
                raise RuntimeError("Unknown operator " + str(tok))
        else:
            raise RuntimeError("Unknown token " + str(tok))

    result = eval_stack.pop()
    if eval_stack:
        raise RuntimeError("The expression is invalid. numbers still in stack. " + str(eval_stack))

    return result


def truth_table(expression, names):
    sorted_names = sorted(names)

    for truth_combo in itertools.product((False, True), repeat=len(sorted_names)):
        values = dict(zip(sorted_names, truth_combo))
        result = compute(expression, values)
        print(values, result)




if __name__ == "__main__":
    while True:
        expression = input('> ')
        tokens = tokenize.tokenize(io.BytesIO(expression.encode('utf-8')).readline)
        rpn = shunting_yard(tokens)

        names = {x.string for x in rpn if x.type == token.NAME}
        print(names)
        print(pretty_rpn(rpn))

        truth_table(rpn, names)
