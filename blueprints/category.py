from flask import Blueprint, abort, jsonify, request, render_template, redirect, url_for
from flask_login import login_required, login_user, logout_user
from common import db, require_permission
from models import Category

category = Blueprint(name='category', url_prefix="/api/category", import_name=__name__)

@category.route('/')
@login_required
@require_permission('ENTITY:CATEGORY:READ')
def getAll():
    categorys = db.session.execute(db.select(Category).order_by(Category.name)).scalars()
    result = [d.as_dict() for d in categorys]
    return result
    
@category.route('/<string:id>', methods = ['GET'])
@login_required
@require_permission('ENTITY:CATEGORY:READ')
def get(id):
    category = db.get_or_404(Category, id)
    return category.as_dict()

@category.route('/', methods = ['POST'])
@login_required
@require_permission('ENTITY:CATEGORY:CREATE')
def create():
    category = Category(
        id=request.form["id"], 
        name=request.form["name"])
    db.session.add(category)
    db.session.commit()
    return category.as_dict()

@category.route('/<string:id>', methods = ['PUT'])
@login_required
@require_permission('ENTITY:CATEGORY:UPDATE')
def update(id:str):
    category:Category = db.get_or_404(Category, id)
    category.id = request.form["id"]
    category.name = request.form["name"]
    db.session.commit()
    return category.as_dict()

@category.route('/<string:id>', methods = ['PATCH'])
@login_required
@require_permission('ENTITY:CATEGORY:UPDATE')
def modify(id:str):
    category:Category = db.get_or_404(Category, id)
    category.name = request.form["name"]
    db.session.commit()
    return category.as_dict()

@category.route('/<string:id>', methods = ['DELETE'])
@login_required
@require_permission('ENTITY:CATEGORY:DELETE')
def delete(id):
    category = db.get_or_404(Category, id)
    db.session.delete(category)
    db.session.commit()
    return category.as_dict()