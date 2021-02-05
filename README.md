# BBLearnTools

Tools in Python for writing math and quizzes for Blackboard Learn.

Packages: currently only one:

* blackjax: for rendering math in Blackboard with Mathjax2.


## Module *blackjax*

[Blackboard Learn](https://www.blackboard.com/teaching-learning/learning-management/blackboard-learn) is a widespread commercial LMS (Learning Management System). LaTeX syntax for math content can be used in blackboard's text editor. This LaTeX code is interpreted by [WIRIS](https://docs.wiris.com/en/mathtype/mathtype_web/latex-support) and rendered with images. The result is not always satisfying. A not very-known alternative is to call locally [Mathjax2](https://docs.mathjax.org/en/v2.7-latest/start.html), instead of the default WIRIS, to render math content. 

*Blackjax* provides tools to convert text written outside of Blackboard Learn, into text whose math can sucessfully be rendered by Mathjax2 within Blackboard Learn.

### Example:

```python
s = r'''Consider the function $f$, periodic with period $2 \, \pi$,
that fulfills:
<br>
$$f(x) = \left\lbrace
\begin{matrix}
1 &  \text{ for } x \in (-\pi;0),\\
-x + 1  & \text{ for } x \in [0;\pi].
\end{matrix}
\right.$$
<br>
Find the coefficient $b_5$ of the Fourier series of $f$.'''
```
Then
```python
blackjaxify(s)
```
gives:
```html
<script type='text/javascript' async src='https://cdn.jsdelivr.net/npm/mathjax@2/MathJax.js?config=TeX-AMS_CHTML'></script>Consider the function \(f\), periodic with period \(2&nbsp;\,&nbsp;\pi\), that fulfills: <br> \begin{equation}f(x)&nbsp;=&nbsp;\left\lbrace&nbsp;\begin{matrix}&nbsp;1&nbsp;&&nbsp;&nbsp;\text{&nbsp;for&nbsp;}&nbsp;x&nbsp;\in&nbsp;(-\pi;0),\\&nbsp;-x&nbsp;+&nbsp;1&nbsp;&nbsp;&&nbsp;\text{&nbsp;for&nbsp;}&nbsp;x&nbsp;\in&nbsp;[0;\pi].&nbsp;\end{matrix}&nbsp;\right.\end{equation} <br> Find the coefficient \(b_5\) of the Fourier series of \(f\).<script type='text/javascript' async src='https://cdn.jsdelivr.net/npm/mathjax@2/MathJax.js?config=TeX-AMS_CHTML'></script>
Consider the function \(f\), periodic with period \(2&nbsp;\,&nbsp;\pi\),
that fulfills:
<br>
\begin{equation}f(x)&nbsp;=&nbsp;\left\lbrace&nbsp;\begin{matrix}&nbsp;1&nbsp;&&nbsp;&nbsp;\text{&nbsp;for&nbsp;}&nbsp;x&nbsp;\in&nbsp;(-\pi;0),\\&nbsp;-x&nbsp;+&nbsp;1&nbsp;&nbsp;&&nbsp;\text{&nbsp;for&nbsp;}&nbsp;x&nbsp;\in&nbsp;[0;\pi].&nbsp;\end{matrix}&nbsp;\right.\end{equation}
<br>
Find the coefficient \(b_5\) of the Fourier series of \(f\).
```
This string can now be copied & pasted in blackboard's editor (in the [source code window](https://help.blackboard.com/Learn/Instructor/Course_Content/Create_Content/Create_Course_Materials/Work_With_Text/What_Does_the_Editor_Do)) or used in pools of questions that can be [uploaded as text files](https://help.blackboard.com/Learn/Instructor/Tests_Pools_Surveys/Reuse_Questions/Upload_Questions).

This is now rendered in Blackboard as:

<img src="IMAGES/blackjax.png" width=1000>

### Installation

* just download the file `blackjax.py` and import it in your python file/interactive session with `from blackjax import blackjaxify`.
* or download and install the whole project `BBLearnTools` by running `python setup.py install`. Then import within python with `from blackjax import blackjaxify`.

