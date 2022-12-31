r"""Tools for uploading to Blackboard Learn texts written in HTML or markdown.

AUTHORS:

- Emmanuel Briand (2021): initial version

`Blackboard Learn <https://www.blackboard.com/teaching-learning/learning-management/blackboard-learn>`_  
is a widespread commercial LMS (Learning Management System). LaTeX 
syntax for math content can be used in blackboard's text editor. 
This LaTeX code can be interpreted by 
`MathType <https://docs.wiris.com/en/mathtype/mathtype_web/latex-support>`_ 
and rendered with images. 
The result is not always satisfying. An not very-known alternative is to use  
`Mathjax2 <https://docs.mathjax.org/en/v2.7-latest/start.html>`_ ,
instead of the default MathType, to render math content. 

*Blackjax* provides a tool (blackjaxify)  to convert text written outside of Blackboard Learn, 
into text whose math can sucessfully be rendered by Mathjax2 within 
Blackboard Learn.

How to use blackjax
-------------------

Example first::

    >>> s = r'''Consider the function $f$, periodic with period $2 \, \pi$,
    ... that fulfills:
    ... <br>
    ... $$f(x) = \left\lbrace
    ... \begin{matrix}
    ... 1 &  \text{ for } x \in (-\pi;0),\\
    ... -x + 1  & \text{ for } x \in [0;\pi].
    ... \end{matrix}
    ... \right.$$
    ... <br>
    ... Find the coefficient $b_5$ of the Fourier series of $f$.'''
    >>> from blackjax import blackjaxify
    >>> print(blackjaxify(s))
    <script type='text/javascript' async src='https://cdn.jsdelivr.net/npm/mathjax@2/MathJax.js?config=TeX-AMS_CHTML'></script>
    Consider the function \(f\), periodic with period \(2&nbsp;\,&nbsp;\pi\),
    that fulfills:
    <br>
    \begin{equation}f(x)&nbsp;=&nbsp;\left\lbrace&nbsp;\begin{matrix}&nbsp;1&nbsp;&&nbsp;&nbsp;\text{&nbsp;for&nbsp;}&nbsp;x&nbsp;\in&nbsp;(-\pi;0),\\&nbsp;-x&nbsp;+&nbsp;1&nbsp;&nbsp;&&nbsp;\text{&nbsp;for&nbsp;}&nbsp;x&nbsp;\in&nbsp;[0;\pi].&nbsp;\end{matrix}&nbsp;\right.\end{equation}
    <br>
    Find the coefficient \(b_5\) of the Fourier series of \(f\).

The steps in general are as follow:

1. save your text as a string, with:

  - for math mode: 

    - math inline mode delimited with:

      - ``$`` ... ``$``
      - or ``\(`` ... ``\)``
  
    - and math display mode with:

      - ``$$`` ... ``$$``
      - or ``\[`` ... ``\]``
      - or ``\begin{equation}`` ... ``\end{equation}`` 
      - or ``\begin{align}`` ... ``\end{align}``
  
  - for text:  you can use HTML syntaxis for your text. Newlines should be 
    indicated explicitly, for instance with `<br>`.


2. load *blackjax.py* and apply the ``blackjaxify`` function to your string. It 
   returns a string that can be copied & pasted in blackboard's editor 
   (in the 
   `source code window <https://help.blackboard.com/Learn/Instructor/Course_Content/Create_Content/Create_Course_Materials/Work_With_Text/What_Does_the_Editor_Do>`_) 
   or used in pools of questions that can be 
   `uploaded as text files <https://help.blackboard.com/Learn/Instructor/Tests_Pools_Surveys/Reuse_Questions/Upload_Questions>`_.
    
What *blackjaxify* does
-----------------------

What *blackjaxify* does:

* inserts a call to Mathjax2

* replaces maths delimiters:

    * inline math delimiters ``$`` .. ``$`` are all replaced with  
      ``\(`` ... ``\)``.
    
    * display math delimiters ``$$`` ... ``$$`` and  ``\[`` ... ``\]`` are all 
      replaced with ``\begin{equation}`` ... ``\end{equation}``.
  
* replaces all newline and whitespace characters in math mode with HTML
  non-breakable spaces ('&nbsp;')
  
If you want to have a newline in the output, use the HTML directive ``<br>``.


The delimiters ``\begin{equation}`` ... ``\end{equation}`` are prefered over 
``\[`` ...  ``\]`` because opening escaped brackets have a special meaning 
for blackboard in some contexts (like FIB_PLUS test questions).

The delimiters ``$`` ... ``$`` and ``$$`` ... ``$$`` are replaced in the output 
because blackboard's math editor WIRIS would render them before Mathjax.

Replacing whitespaces and newline characters in math mode prevents blackboard 
from inserting HTML linebreak directives that would break the math code before 
Mathjax tries to render it.

.. warning:: Nested math modes, as in 
   ``r'\(f(x) = 1 \text{ if \(x > 0\), otherwise }0.\)'`` 
   are not supported. Avoid them. 
"""
# imports
#----------
import re

# constants
#----------
_MATHJAX_URL = 'https://cdn.jsdelivr.net/npm/mathjax@2/MathJax.js?config=TeX-AMS_CHTML'
_DELIMITERS = [(r'\(', r'\)'), 
               (r'\begin{equation}', r'\end{equation}'),
               (r'\begin{align}', r'\end{align}')
              ]

# Main function
#---------------------

def blackjaxify(text, script=True, script_url=_MATHJAX_URL, escape_brackets=False):
    r"""
    Return a formatted copy of ``text`` suitable for uploading in blackboard
    
    INPUT:
        - ``text`` -- string
        - ``script`` -- boolean (Default: ``True``)
        - ``script_url`` -- string (Default: ``_MATHJAX_URL``)
        - ``escape_brackets`` -- boolean (Default:  ``False``)
    """
    if script:
    	text = insert_mathjax_script(text, script_url)
    text = fix_latex_delimiters(text)
    if escape_brackets:
        text = escape_opening_brackets(text) 
    text = remove_spaces_in_latex(text) 
    return text

def insert_mathjax_script(text, url=_MATHJAX_URL):
    """
    Return a copy of ``text`` with a script calling MathJax2 added at the 
    beginning.
    
    The default url does the job, but another url may be used, for instance 
    the url of a local script.
    """
    mathjax = (r"<script type='text/javascript' async src='{url}'></script>" 
               + "\n").format(url=url)
    return mathjax + text

def escape_opening_brackets(text):
    r"""
    Replace all occurrences of opening bracket '[' with '\[', except those 
    between <pre> and </pre>
    
    Blackboard needs all opening brackets to be escaped when uploading a test 
    or a pool as a text file. (except for those in a <pre></pre> environnment).
    This is not the case for closing brackets.
    
    Needed for some types of questions such as FIB_PLUS.
    """
    return text.replace('[', r'\[')

def replace_inside(s, opening, closing, before=" ", after="&nbsp;"):
    r"""
    Return the string obtained from ``s`` by replacing ``before`` with ``after`` 
    in all substrings delimited by  ``opening`` and ``closing``.
    
    Replace spaces with HTML non-breakable spaces when between escaped brackets::
    
        >>> s = r"\[ L[1] = 2 \]"; replace_inside(s, r'\[', r'\]')
        '\\[&nbsp;L[1]&nbsp;=&nbsp;2&nbsp;\\]'
        
    Replace ``**`` with ``^``  when between dollars::
    
        >>> s = r"**Note that:** $ 2**2 = 4$."
        >>> replace_inside(s, '$', '$', '**', '^')
        '**Note that:** $ 2^2 = 4$.'
    """
    opening = re.escape(opening)
    closing = re.escape(closing)
    inside = re.compile((r'({opening}.*?{closing})'
                         .format(opening=opening,closing=closing)),
                        re.DOTALL)
    return re.sub(inside, lambda x: x.group(1).replace(before, after), s)

def fix_latex_delimiters(text):
    r"""
    Return the string obtained by replacing the LaTeX delimiters 
    ``$`` ... ``$`` with ``\(`` ... ``\)`` 
    and ``$$`` ... ``$$`` with ``\begin{equation}`` ... ``\end{equation}``.
    
    Uses the python module ``re`` (regular expressions).
    
    .. warning:: This function substitutes as well escaped dollars. 
        
    EXAMPLES::
    
        >>> fix_latex_delimiters("$1+1=2$.")
        '\\(1+1=2\\).'
        
        >>> fix_latex_delimiters("$$1+1=2$$")
        '\\begin{equation}1+1=2\\end{equation}'
        
    In the following example, the current code would return erroneously 
    ``'Price: 2\\\\(. But \\)2+2=4$.'``. 
    A ``NotImplemented Error`` is returned instead::
    
        >>> fix_latex_delimiters(r"Price: 2\$. But $2+2=4$.")
        Traceback (most recent call last):
        ...
        NotImplementedError: The string contains escaped dollars.
        
    .. note:: Another implementation is suggested 
       `here <https://stackoverflow.com/questions/48361541/convert-latex-dollar-sign-to>`_ 
       and 
       `there <https://stackoverflow.com/questions/14949090/in-python-how-can-i-use-regex-to-replace-square-bracket-with-parentheses>`_ .
       This is (for pair of matching simple dollars):
       ``re.sub(r'(^|[^\$])\$([^\$]+)\$([^\$]|$)',r'\1\\(\2\\)\3', text)``
    """
    if re.search(r"\\\$", text) != None:
        raise NotImplementedError("The string contains escaped dollars.")
    text = re.sub(r"\${2}(.+?)\${2}", r"\\begin{equation}\1\\end{equation}" ,
                  text, flags = re.DOTALL) 
    text = re.sub(r"\${1}(.+?)\${1}", r"\(\1\)" , text, flags = re.DOTALL)
    return text

def remove_spaces_in_latex(text):
    r"""
    Return a copy of the text with all spaces and newline characters
    thata are between LaTeX math mode delimiters are
    replaced with HTML nonbreakable spaces '&nbsp;'.
    
    The LaTeX math delimiters affected are:
    
    - ``\(``... ``\)``
    - ``\begin{equation}`` ... ``\end{equation}``
    - ``\begin{align}`` ... ``\end{align}``    
        
    EXAMPLES::
    
        >>> remove_spaces_in_latex('\(1 + 1 = 2\)')
        '\\(1&nbsp;+&nbsp;1&nbsp;=&nbsp;2\\)'
        
    .. warning:: Nested math modes are not supported.       
        
    Example of failure with nested math (note the whitespace left before 
    "otherwise")::

        >>> s = r'\(f(x) = 1 \text{ if \(x > 0\), otherwise }0.\)'
        >>> remove_spaces_in_latex(s)
        '\\(f(x)&nbsp;=&nbsp;1&nbsp;\\text{&nbsp;if&nbsp;\\(x&nbsp;>&nbsp;0\\), otherwise }0.\\)'
        
    """
    for (opening, closing) in _DELIMITERS:
        text = replace_inside(text, opening, closing, ' ', '&nbsp;')
        text = replace_inside(text, opening, closing, '\n', '&nbsp;')
    return text
