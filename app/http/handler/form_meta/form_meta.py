from flask import jsonify, request, url_for
from app.http.handler.form_meta import form_meta_blueprint
from app.core.controllers.form_meta_controller import find_form_meta, delete_form_meta, insert_form_meta, request_to_class,\
     to_json_list, find_form_metas
from flask_pymongo import ObjectId
from app.core.controllers.common_controller import dict_serializable, UrlCondition, Paginate, sort_limit
from pymongo.errors import ServerSelectionTimeoutError, PyMongoError, OperationFailure


@form_meta_blueprint.route('/form_metas', methods=['POST'])
def new_form_meta():
    from run import mongo
    form_meta = request_to_class(request.json)
    try:
        insert_form_meta(mongo, form_meta)
    except ServerSelectionTimeoutError as e:
        return jsonify({
            'code': 500,
            'message': str(e),
            'form_meta':None
        }),500
    return jsonify({
        'code':200,
        'message':'',
        'form_meta': None
    }),200


@form_meta_blueprint.route('/form_metas')
def get_form_metas():
    url_condition = UrlCondition(request.args)
    from run import mongo
    try:
        form_metas = find_form_metas(mongo, url_condition.filter_dict)
    except PyMongoError as e:
        return jsonify({
            'code':500,
            'message': str(e),
            'form_meta':None
        }),500
    form_metas = sort_limit(form_metas, url_condition.sort_limit_dict)
    paginate = Paginate(form_metas, url_condition.page_dict)
    form_metas_list = [to_json_list(form_meta) for form_meta in paginate.data_page]
    prev = None
    if paginate.has_prev:
        prev = url_for('form_meta_blueprint.get_form_metas', _page=paginate.page - 1)
    next = None
    if paginate.has_next:
        next = url_for('form_meta_blueprint.get_form_metas', _page=paginate.page + 1)
    return jsonify({
        'code':200,
        'message':'',
        'form_metas':[dict_serializable(form_metas_list_node) for form_metas_list_node in form_metas_list],
        'prev': prev,
        'next': next,
        'has_prev': paginate.has_prev,
        'has_next': paginate.has_next,
        'total': paginate.total,
        'page_num': paginate.page_num,
        'page_now': paginate.page,
        'per_page': paginate.per_page
    }),200

@form_meta_blueprint.route('/form_metas/<string:_id>')
def get_form_meta(_id):
    from run import mongo
    try:
        form_meta = find_form_meta(mongo, _id)
    except PyMongoError as e:
        return jsonify({
            'code':500,
            'message':str(e),
            'form_meta':None
        }),500
    if form_meta is None:
        return jsonify({
            'code':404,
            'message':'not found',
            'form_meta':None
        }),404
    return jsonify({
        'code':200,
        'message':'',
        'form_meta':dict_serializable(form_meta) if form_meta is not None else None
    }),200


@form_meta_blueprint.route('/form_metas/<string:_id>', methods=['DELETE'])
def delete_from_meta(_id):
    from run import mongo
    form_meta = find_form_meta(mongo, _id)
    if form_meta is None:
        return jsonify({
            'code':404,
            'message':'not found',
            'form_meta':None
        }),404
    try:
        delete_form_meta(mongo, {'_id':ObjectId(_id)})
    except PyMongoError as e:
        return jsonify({
            'code':500,
            'message':str(e),
            'farm_meta':None
        }),500
    return jsonify({
        'code':200,
        'message':'',
        'form_meta':None
    }),200


@form_meta_blueprint.route('/form_metas/<string:_id>', methods=['PUT'])
def change_form_meta(_id):
    from run import mongo
    form_meta = find_form_meta(mongo, _id)
    if form_meta is None:
        return jsonify({
            'code':404,
            'message':'not found',
            'form_meta':None
        }),404
    try:
        delete_form_meta(mongo, {'_id':ObjectId(_id)})
    except PyMongoError as e:
        return jsonify({
            'code':500,
            'message':str(e),
            'form_meta': None
        }),500
    form_meta = request_to_class(request.json)
    try:
        insert_form_meta(mongo, form_meta)
    except ServerSelectionTimeoutError as e:
        return jsonify({
            'code': 500,
            'message': str(e),
            'form_meta': None
        }),500
    return jsonify({
        'code': 200,
        'message': '',
        'form_meta': None
    }),200
