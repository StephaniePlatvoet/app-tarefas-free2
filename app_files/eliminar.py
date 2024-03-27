from flask import redirect, url_for


def eliminar(task_class,db,id):
    task_class.query.filter_by(id=int(id)).delete()
    db.session.commit()
    return redirect(url_for('go_home') + '#content')