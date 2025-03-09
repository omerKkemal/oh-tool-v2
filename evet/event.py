from flask import Blueprint,jsonify,request,render_template

event = Blueprint('event',__name__,template_folder='templates',static_folder='static',static_url_path='/static')

@event.route('/api/404')
def api_404():
    return jsonify({"error":"404 page not found"})


@event.route('/api/500')
def api_500():
    return jsonify({"error":"500 internal server error"})


@event.route('/error-404')
def page_404():
    return render_template('error-404.html')


@event.route('/error-500')
def page_500():
    return render_template('error-500.html')