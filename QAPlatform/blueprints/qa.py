from flask import Blueprint, render_template, request, redirect, g, url_for
from .forms import QuestionForm, AnswerForm
from models import QuestionModel, AnswerModel
from exts import db
from login_decorator import login_request


bp = Blueprint('qa', __name__, url_prefix='/')


@bp.route('/')
def index():
    # order_by(QuestionModel.create_time.desc())是倒序展示所有数据
    questions = QuestionModel.query.order_by(QuestionModel.create_time.desc()).all()
    return render_template('index.html', questions=questions)


@bp.route('/qa/public', methods=['GET', 'POST'])
@login_request
# 渲染问答列表
def public_question():
    if request.method == 'GET':
        return render_template('public_question.html')
    else:
        # form=页面提交的表单内容
        form = QuestionForm(request.form)
        # 判断表单内容是否存在
        if form.validate():
            title = form.title.data
            content = form.content.data
            qusetion = QuestionModel(title=title, content=content, author=g.user)
            db.session.add(qusetion)
            db.session.commit()
            return redirect('/')
        else:
            print(form.errors)
            return redirect(url_for('qa.public_question'))


# 问答详情页
@bp.route('/detail/<question_id>')
def qa_detail(question_id):
    question = QuestionModel.query.get(question_id)
    return render_template('detail.html', question=question)


# 评论
# @bp.route('/answer/public', methods=['POST'])
@bp.post('/answer/public')
@login_request
def public_answer():
    form = AnswerForm(request.form)
    if form.validate():
        content = form.content.data
        question_id = form.question_id.data
        answer = AnswerModel(content=content, question_id=question_id, author_id=g.user.id)
        db.session.add(answer)
        db.session.commit()
        return redirect(url_for("qa.qa_detail", question_id=question_id))
    else:
        print(form.errors)
        # question_id=request.form.get('question_id')是因为当上面form传空时就会没有question_id
        # request.form.get()就一定会有
        return redirect(url_for("qa.qa_detail", question_id=request.form.get('question_id')))


# 搜索功能
@bp.route('/search')
def search():
    # 有以下几种方法实现
    # /search?q=flask 用这种最简单
    # /search/<q>
    # post, request.form
    q = request.args.get('q')
    # 根据标题查找
    questions = QuestionModel.query.filter(QuestionModel.title.contains(q)).all()
    return render_template('index.html', questions=questions)