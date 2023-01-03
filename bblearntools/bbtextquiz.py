r"""Functions for creating quizzes for Blackboard, to be uploaded as text files.

AUTHORS:

- Emmanuel Briand (2021): initial version

The function ``write_bbtextpool`` writes a text file than can be uploaded in Blackboard Learn (ORIGINAL course view) as indicated in Blackboard\'s help pages on "`Upload Questions
<https://help.blackboard.com/Learn/Instructor/Original/Tests_Pools_Surveys/Orig_Reuse_Questions/Upload_Questions>`_" 
to create a pool of questions. 

The functions `fields_NUM`, `fields_MC`, `fields_MA`, `fields_TF` format the questions 
of type NUM, MC, MA and TF. See the aforementionned BlackBoard help page.

EXAMPLES:

We create a pool of four questions, of types MC, MA, NUM and TF::

    >>> q = r'For $F(x,y)=x^2 y - x^2 - 2 y^2 + 3$, ¿What type of point is $(2;1)$?'
    >>> Q1 = fields_MC(q, [('a local maximum', False), 
    ...                    ('a local minimum', False), 
    ...                    ('a saddle point', True)])
    >>> Q2 = fields_MA('¿Which of the following functions are even?', 
    ...                 [('cosine', True), ('sine', False), ('$x^2$', True), ('$x+1$', False)])
    >>> Q3 = fields_TF('The series with general term $1/n$ is convergent.', False )
    >>> q = r'''¿What is the infinite sum  
    ... $1+\frac{1}{5} + \frac{1}{25}+ \frac{1}{125} + \cdots$?
    ... <br>
    ... Give your answer with two decimal places.'''
    >>> Q4 = fields_NUM(q, 1.25, 0.01)
    >>> write_bbpool('TESTS/pool4.txt', [Q1, Q2, Q3, Q4]) # doctest:   +SKIP

We create a pool of 16 questions of type NUM whose data are different. 
For this, we make use of `Template strings <https://docs.python.org/3.8/library/string.html#template-strings>`_::

    >>> from string import Template
    >>> class BBTemplate(Template):
    ...     delimiter = r'\temp'
    >>> q = BBTemplate(r"How many \temp{type} pairs of distinct elements of $\{1, 2, \ldots, \temp{n}\}$ are there?")
    >>> def ans(type, n): return int(n*(n-1)/2) if type == 'unordered' else n*(n-1)
    >>> L = [fields_NUM(q.substitute(type=type, n=n), ans(type, n)) 
    ...      for n in range(7, 15) for type in ['ordered', 'unordered']]
    >>> write_bbpool('TESTS/pool_on_pairs.txt', L) # doctest:   +SKIP
    >>> len(L)
    16
    >>> L[0] # Let us a look at the first question
    ['NUM', "<script type='text/javascript' async src='https://cdn.jsdelivr.net/npm/mathjax@2/MathJax.js?config=TeX-AMS_CHTML'></script> How many ordered pairs of distinct elements of \\(\\{1,&nbsp;2,&nbsp;\\ldots,&nbsp;7\\}\\) are there?", '42', '0']
    
Metadata
--------

Note that you cannot associate metadata (such as: feedback, or partial credir) to the questions uploaded this way. To upload questions with Metadata, you need to **import** your questions as explained in the BlackBoard help pages on `"Import_or_Export_Tests_Surveys_and_Pools" <https://help.blackboard.com/Learn/Instructor/Original/Tests_Pools_Surveys/Reuse_Questions/Import_or_Export_Tests_Surveys_and_Pools>`_. Files to be imported need to be written in a format proper to Blackboard. To write such files, you need a Blackboard quiz maker such as  `toasted crumpets\' Blackboard Quiz Maker <https://github.com/toastedcrumpets/BlackboardQuizMaker>`_ or the commercial tool `Respondus 4.0 <https://web.respondus.com/he/respondus/>`_.

About the decimal separator (comma/dot)
---------------------------------------

The decimal separator for a course in BlackBoard Learn depends on the language pack used in this course. The questions uploaded in blackboard must fit this option. The default decimal separator in ``bbtextquiz.py`` is the comma. You can change this by running ``set_decimal_separator('.')``.

EXAMPLE:

    >>> q = r'''¿What is the infinite sum  
    ... $1+\frac{1}{5} + \frac{1}{25}+ \frac{1}{125} + \cdots$?
    ... <br>
    ... Give your answer with two decimal places.'''
    >>> fields_NUM(q, 1.25, 0.01)
    ['NUM', "<script type='text/javascript' async src='https://cdn.jsdelivr.net/npm/mathjax@2/MathJax.js?config=TeX-AMS_CHTML'></script> ¿What is the infinite sum   \\(1+\\frac{1}{5}&nbsp;+&nbsp;\\frac{1}{25}+&nbsp;\\frac{1}{125}&nbsp;+&nbsp;\\cdots\\)? <br> Give your answer with two decimal places.", '1,25', '0,01']
    >>> set_decimal_separator('.')
    Decimal separator set to .
    >>> fields_NUM(q, 1.25, 0.01)
    ['NUM', "<script type='text/javascript' async src='https://cdn.jsdelivr.net/npm/mathjax@2/MathJax.js?config=TeX-AMS_CHTML'></script> ¿What is the infinite sum   \\(1+\\frac{1}{5}&nbsp;+&nbsp;\\frac{1}{25}+&nbsp;\\frac{1}{125}&nbsp;+&nbsp;\\cdots\\)? <br> Give your answer with two decimal places.", '1.25', '0.01']
    >>> set_decimal_separator() # back to ','as separator
    Decimal separator set to ,

"""

# imports
#--------
import csv
csv.register_dialect('blackboard', delimiter='\t', quoting=csv.QUOTE_NONE)
from itertools import chain
from blackjax import blackjaxify

# global setting
#---------------
options = {'decimal separator': ','}
print("Decimal separator: ", options['decimal separator'])

def set_decimal_separator(sep = ','):
    r"""Change the decimal separator.

    INPUT:

    - ``sep`` -- string (Default: ','). Muest be either ',' or '.'
 
    EXAMPLES:

    >>> options['decimal separator']
    ','
    >>> set_decimal_separator('.')
    Decimal separator set to .
    >>> options['decimal separator']
    '.'
    >>> set_decimal_separator()
    Decimal separator set to ,
    >>> options['decimal separator']
    ','
"""
    if sep not in [',', '.']:
        raise ValueError('Argument of set_decimal_separator should be either "."\
         or ",", got', sep)
    else:
        options['decimal separator'] = sep
        print("Decimal separator set to", sep)
         
# formatting
#------------

def _format_string(str, script=True):
    r"""
    Remove newline characters and format math so that it can be rendered by Mathjax2.
    """
    str = blackjaxify(str, script)
    str = str.replace('\n', ' ')
    # Note that
    # removing newline chars must be done AFTER blackjaxifying
    # since blackjaxify inserts a newline char.
    return str
    
def _fix_decimal_separator(x):
    r"""
    Return the string representing x, with decimal comma, instead of decimal 
    point.
    
    INPUT:
    
    - ``x`` -- floating point number
       
    OUTPUT: a string.
    
    TODO: use d
    
    EXAMPLES:
    
        >>> _fix_decimal_separator(1.5)
        '1,5'
        >>> from math import sqrt
        >>> _fix_decimal_separator(sqrt(2))
        '1,4142135623730951'
    """
    if options['decimal separator'] == ',':
        return str(x).replace('.', ',')
    else:
        return str(x)
    
# types of questions
#-------------------
    
def fields_NUM(question, answer, tol=0):
    r"""Return a version of the arguments formatted as a Numerical (NUM) question for blackboard.
    
    INPUT:
    
    - ``question`` -- string.
    
    - ``answer`` -- a number.
    
    - ``tol`` -- a number (Default: 0). Not in scientific notation.
    
    EXAMPLES:

    A question whose answer is an approximation::

        >>> q = r'''¿What is the infinite sum  
        ... $1+\frac{1}{5} + \frac{1}{25}+ \frac{1}{125} + \cdots$?
        ... <br>
        ... Give your answer with two decimal places. 
        ... Use decimal comma (as in $3,14$)  rather than decimal point <s>(3.14)</s>.'''
        >>> fields_NUM(q, 1.25, 0.01)
        ['NUM', "<script type='text/javascript' async src='https://cdn.jsdelivr.net/npm/mathjax@2/MathJax.js?config=TeX-AMS_CHTML'></script> ¿What is the infinite sum   \\(1+\\frac{1}{5}&nbsp;+&nbsp;\\frac{1}{25}+&nbsp;\\frac{1}{125}&nbsp;+&nbsp;\\cdots\\)? <br> Give your answer with two decimal places.  Use decimal comma (as in \\(3,14\\))  rather than decimal point <s>(3.14)</s>.", '1,25', '0,01']
        
    Use dot instead of comma as separator::
     
	>>> set_decimal_separator('.')
        Decimal separator set to .
	>>> fields_NUM(q, 1.25, 0.01)
	['NUM', "<script type='text/javascript' async src='https://cdn.jsdelivr.net/npm/mathjax@2/MathJax.js?config=TeX-AMS_CHTML'></script> ¿What is the infinite sum   \\(1+\\frac{1}{5}&nbsp;+&nbsp;\\frac{1}{25}+&nbsp;\\frac{1}{125}&nbsp;+&nbsp;\\cdots\\)? <br> Give your answer with two decimal places.  Use decimal comma (as in \\(3,14\\))  rather than decimal point <s>(3.14)</s>.", '1.25', '0.01']
        >>> set_decimal_separator() # back to ',' as separator    
        Decimal separator set to ,
    """
    question =  _format_string(question)
    answer = _fix_decimal_separator(answer)
    tol = _fix_decimal_separator(tol)
    return ['NUM', question, answer, tol] 

def fields_MA(question, answers):
    r"""Return a version of the arguments formatted as a Multiple Answer (MA) question for blackboard.
    
    INPUT:
    
    - ``question`` -- string
    
    - ``answers``-- list of pairs  (``s``, ``b``), 
      where ``s`` is a string (proposed answer) and ``b`` a boolean. 

    EXAMPLE::

        >>> fields_MA('Which of the following functions are even?', 
        ...           [('cosine', True), ('sine', False), ('$x^2$', True), ('$x+1$', False)])
        ['MA', "<script type='text/javascript' async src='https://cdn.jsdelivr.net/npm/mathjax@2/MathJax.js?config=TeX-AMS_CHTML'></script> Which of the following functions are even?", 'cosine', 'correct', 'sine', 'incorrect', '\\(x^2\\)', 'correct', '\\(x+1\\)', 'incorrect']
    """
    question = _format_string(question)
    answers = [(_format_string(s, script=False), b) for (s, b) in answers ]
    return (['MA', question ] 
            + list(chain.from_iterable([s, "correct" if b else "incorrect"]
               for (s, b) in answers)))

def fields_MC(question, answers):
    r"""Return a version of the arguments formatted as a Multiple Choice (MC) question for blackboard.
    
    INPUT:
    
    - ``question`` -- string
    
    - ``answers``-- list of pairs  (``s``, ``b``), 
      where ``s`` is a string (proposed answer) and ``b`` a boolean.  
      Exactly one of the proposed answers should have value ``True``, else an error is raised.

    EXAMPLE::

        >>> q = r'For $F(x,y)=x^2 y - x^2 - 2 y^2 + 3$, What type of point is $(2;1)$?'
        >>> fields_MC(q, [('a local maximum', False), 
        ...               ('a local minimum', False), 
        ...               ('a saddle point', True)])
        ['MC', "<script type='text/javascript' async src='https://cdn.jsdelivr.net/npm/mathjax@2/MathJax.js?config=TeX-AMS_CHTML'></script> For \\(F(x,y)=x^2&nbsp;y&nbsp;-&nbsp;x^2&nbsp;-&nbsp;2&nbsp;y^2&nbsp;+&nbsp;3\\), What type of point is \\((2;1)\\)?", 'a local maximum', 'incorrect', 'a local minimum', 'incorrect', 'a saddle point', 'correct']
    """
    if [b for (s, b) in answers].count(True) != 1:
        raise ValueError("Exactly one of the proposed answers should be marked as True.")
    if [b for (s, b) in answers].count(False) != len(answers)-1:
        raise ValueError("All proposed answers except the correct one should be marked as False")
    question = _format_string(question)
    answers = [(_format_string(s, script=False), b) for (s, b) in answers ]
    return (['MC', question] 
            + list(chain.from_iterable([s, "correct" if b else "incorrect"]
               for (s, b) in answers)))
               
def fields_TF(question, ans):
    r"""Return a version of the arguments formatted as a True/False (TF) question for blackboard.
    
    INPUT:
    
    - ``question`` -- string
    
    - ``ans`` -- boolean

    EXAMPLE::

        >>> fields_TF('The series with general term $1/n$ is convergent.', False )
        ['TF', "<script type='text/javascript' async src='https://cdn.jsdelivr.net/npm/mathjax@2/MathJax.js?config=TeX-AMS_CHTML'></script> The series with general term \\(1/n\\) is convergent.", 'False']
    """
    question = _format_string(question)
    return ['TF', question, str(ans)]
    
def fields_ESS(question, sample_ans=""):
    r"""Return a version of the arguments formatted as an Essay question (ESS) for blackboard.
    
    INPUT:
    
    - ``question`` -- string.
    
    - ``sample_ans`` -- string (Default: "").
    
    EXAMPLE::

        >>> fields_ESS("Give a few examples where you can help preserve marine ecosystems.")
        ['ESS', "<script type='text/javascript' async src='https://cdn.jsdelivr.net/npm/mathjax@2/MathJax.js?config=TeX-AMS_CHTML'></script> Give a few examples where you can help preserve marine ecosystems.", "<script type='text/javascript' async src='https://cdn.jsdelivr.net/npm/mathjax@2/MathJax.js?config=TeX-AMS_CHTML'></script> "]

    """
    question =  _format_string(question)
    sample_ans = _format_string(sample_ans)
    return ['ESS', question, sample_ans]


def fields_SR(question, sample_ans=""):
    r"""Return a version of the arguments formatted as an Essay question (ESS) for blackboard.
    
    INPUT:
    
    - ``question`` -- string.
    
    - ``sample_ans`` -- string (Default: "").
    
    EXAMPLE::

        >>> fields_SR("Which ocean species do you find most interesting? Give three facts about it. ")
        ['SR', "<script type='text/javascript' async src='https://cdn.jsdelivr.net/npm/mathjax@2/MathJax.js?config=TeX-AMS_CHTML'></script> Which ocean species do you find most interesting? Give three facts about it. ", "<script type='text/javascript' async src='https://cdn.jsdelivr.net/npm/mathjax@2/MathJax.js?config=TeX-AMS_CHTML'></script> "]
    """
    question =  _format_string(question)
    sample_ans = _format_string(sample_ans)
    return ['SR', question, sample_ans]

def fields_FIL(question):
    r"""Return a version of the arguments formatted as a File question (FIL) for Blackboard.
    
    INPUT:
    
    - ``question`` -- string.
      
    EXAMPLE::

        >>> fields_FIL("What is the average temperature of the Pacific Ocean?")
        ['FIL', "<script type='text/javascript' async src='https://cdn.jsdelivr.net/npm/mathjax@2/MathJax.js?config=TeX-AMS_CHTML'></script> What is the average temperature of the Pacific Ocean?"]
    """
    question =  _format_string(question)
    return ['FIL', question]
    
def fields_ORD(*args):
    raise NotImplementedError
    
def fields_MAT(*args):
    raise NotImplementedError
    
def fields_FIB(*args):
    raise NotImplementedError
    
def fields_FIB_PLUS(*args):
    raise NotImplementedError
    
def fields_OP(*args):
    raise NotImplementedError
    
def fields_JUMBLED_SENTENCE(*args):
    raise NotImplementedError
    
def fields_QUIZ_BOWL(*args):
    raise NotImplementedError
                         
# write in files
#-----------------

def write_bbpool(output_file, fields_list):
    r"""Write the questions in a text file suitable for uploading in Blackboard.
    
    EXAMPLE::
    
        >>> q = r'For $F(x,y)=x^2 y - x^2 - 2 y^2 + 3$, What type of point is $(2;1)$?'
        >>> Q1 = fields_MC(q, [('a local maximum', False), 
        ...                    ('a local minimum', False), 
        ...                    ('a saddle point', True)])
        >>> Q2 = fields_TF('The series with general term $1/n$ is convergent.', False )
        >>> write_bbpool('TESTS/short_test.txt', [Q1, Q2]) # doctest:   +SKIP
        
    """
    with open(output_file, "w", encoding='utf-16') as f:
        writer = csv.writer(f, dialect='blackboard')
        writer.writerows(fields_list)

def render_in_file(output, file):
    r"""Write all questions in an HTML file.
    
    This HTML file can be consulted to check that the math formulas
    are well processed.
    
    This does not completely guarantee that they will be well processed inside
    Blackboard.
    """
    res = (r'<html><head><meta charset="UTF-8"></head><body>{}</body ></html>'
           .format(output))
    with open(file, 'w') as f:
        f.write(res)
